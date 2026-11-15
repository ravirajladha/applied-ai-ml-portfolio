% =====================================================================
% AIMLCZG557 / AECLZG557  -  Assignment 2  -  PS5  -  COVID-19
% Disease diagnosis expert system built from the given decision tree.
%
% Group Id   : Gxxx        <-- fill in before submitting
% Members    : <name>, <name>, <name>, <name>
%
% How to run:
%   swipl -q -g main -t halt PS05.pl < inputPS05.txt
% or interactively:
%   swipl PS05.pl
%   ?- main.
%
% The program asks 4 questions, walks the decision tree, prints the
% predicted disease and also writes it to outputPS05.txt.
% =====================================================================


% =====================================================================
% SECTION 1 : KNOWLEDGE BASE (FACTS)
% =====================================================================

% Temperature in F at or above which a fever counts as "high".
fever_threshold(100.4).

% The name of the file the results are written to.
output_file('outputPS05.txt').

% The four attributes we ask about, in the order they are asked.
attribute_order([fever, cough, pain, rash]).

% Question text. Kept exactly as given in the problem statement.
question(fever, 'Is the Fever Intensity (high_sudden/high/mild/none)? ').
question(cough, 'Is the Cough Type (severe_dry/persistent_dry/mild/none)? ').
question(pain,  'Is the Body Pain Severity (severe/excruciating/mild/none)? ').
question(rash,  'Is the Skin Rash Type (absent/patchy)? ').

% Answers we accept for each attribute. Anything else is rejected.
allowed(fever, [high_sudden, high, mild, none]).
allowed(cough, [severe_dry, persistent_dry, mild, none]).
allowed(pain,  [severe, excruciating, mild, none]).
allowed(rash,  [absent, patchy]).

% ---- Decision tree node 1 : is the fever high? ----
high_fever(high_sudden).
high_fever(high).

% ---- Decision tree node 2 : is there a skin rash? ----
rash_present(patchy).

% ---- Node 3 (left branch)  : "Severe Body Pain & Hacking Cough" ----
severe_pain(severe).
severe_pain(excruciating).
hacking_cough(severe_dry).

% ---- Node 4 : "Is Taste/Smell Lost?"
% Only 4 attributes are asked, so taste/smell is not a direct question.
% The severity matrix lists "Persistent, Dry" as the COVID-19 cough, so
% that cough type stands in for the "Taste/Smell Lost = Yes" branch.
taste_smell_lost(persistent_dry).

% ---- Node 5 : mild answers, used on the low/mild fever path ----
mild_symptom(mild).
mild_symptom(none).

% Display names for each leaf of the tree.
disease_name(influenza,   'Influenza').
disease_name(covid19,     'COVID-19').
disease_name(dengue,      'Dengue').
disease_name(common_cold, 'Common Cold').
disease_name(other_virus, 'Other Viral Infection').
disease_name(allergies,   'Allergies / Other Infection').


% =====================================================================
% SECTION 2 : DECISION TREE RULES
% =====================================================================
% diagnose(+Fever, +Cough, +Pain, +Rash, -Disease)
% Clauses are written in the same top-down order as the tree, so the
% first clause that matches is the branch the tree would have taken.
% The cut (!) stops Prolog backtracking into a lower branch.

% ---------------- HIGH FEVER PATH ----------------
% Node 2 : high fever + patchy rash -> Dengue.
diagnose(F, _, _, R, dengue) :-
    high_fever(F),
    rash_present(R),
    !.

% Node 4a : severe body pain + hacking cough, taste/smell kept -> Influenza.
diagnose(F, C, P, _, influenza) :-
    high_fever(F),
    hacking_cough(C),
    severe_pain(P),
    !.

% Node 4b : persistent dry cough = taste/smell lost -> COVID-19.
diagnose(F, C, _, _, covid19) :-
    high_fever(F),
    taste_smell_lost(C),
    !.

% Node 4c : high fever, no rash, nothing distinctive -> Other Viral Infection.
diagnose(F, _, _, _, other_virus) :-
    high_fever(F),
    !.

% ---------------- LOW / MILD FEVER PATH ----------------
% A rash is not a Common Cold symptom, so it leaves the cold branch.
diagnose(_, _, _, R, allergies) :-
    rash_present(R),
    !.

% Node 5 : mild cough / sore throat and mild body aches -> Common Cold.
diagnose(_, C, P, _, common_cold) :-
    mild_symptom(C),
    mild_symptom(P),
    !.

% Anything else with little or no fever.
diagnose(_, _, _, _, allergies).


% =====================================================================
% SECTION 3 : READING AND VALIDATING THE ANSWERS
% =====================================================================

% safe_read(-Term)
% Reads one answer and always returns something ground.
% Two things can go wrong:
%   - the text is not a legal term  -> read/1 throws, so we catch it;
%   - the text starts with a capital (High_sudden) -> Prolog reads that
%     as a VARIABLE, which would unify with any allowed value and be
%     accepted silently. So an unbound answer is rejected too.
% Both become the marker 'malformed_answer'.
safe_read(Term) :-
    catch(read(Raw), _Error, Raw = malformed_answer),
    (   var(Raw)
    ->  Term = malformed_answer
    ;   Term = Raw
    ).

% normalise_fever(+Raw, -Value)
% The prompt asks for a word, but a plain temperature (e.g. 101.9) is
% also accepted and converted using the 100.4 F threshold.
normalise_fever(Raw, high) :-
    number(Raw),
    fever_threshold(T),
    Raw >= T,
    !.
normalise_fever(Raw, mild) :-
    number(Raw),
    !.
normalise_fever(Value, Value).

% convert(+Attribute, +Raw, -Value)
% Only the fever answer needs converting; the rest are used as typed.
convert(fever, Raw, Value) :-
    !,
    normalise_fever(Raw, Value).
convert(_, Value, Value).

% validate(+Attribute, +Value, -Accepted)
% Accept a known value, otherwise report the problem and ask again.

% The answer was not even readable Prolog (bad spelling, missing dot).
validate(Attr, malformed_answer, Accepted) :-
    !,
    allowed(Attr, List),
    format('~n  [error] that answer could not be read. Expected one of ~w.~n',
           [List]),
    ask(Attr, Accepted).
validate(Attr, Value, Value) :-
    allowed(Attr, List),
    memberchk(Value, List),
    !.
validate(Attr, Value, Accepted) :-
    allowed(Attr, List),
    format('  [error] "~w" is not a valid answer. Expected one of ~w.~n',
           [Value, List]),
    ask(Attr, Accepted).

% from_file
% True when the answers come from a redirected file rather than a keyboard.
from_file :-
    \+ stream_property(user_input, tty(true)).

% echo_answer(+Raw)
% A terminal echoes what the user types, a redirected file does not.
% So for file input we print the answer ourselves to keep the transcript
% looking like the sample (prompt and answer on the same line).
echo_answer(malformed_answer) :-
    !.
echo_answer(Raw) :-
    (   from_file
    ->  format('~w.', [Raw])
    ;   true
    ),
    nl.

% input_left
% True while another case may still follow. With a file we skip blank
% space and look ahead, so no prompt is printed after the last case.
% On a terminal looking ahead would block, so we simply carry on.
input_left :-
    \+ from_file,
    !.
input_left :-
    peek_char(Ch),
    Ch \== end_of_file,
    (   char_type(Ch, space)
    ->  get_char(_),
        input_left
    ;   true
    ).

% ask(+Attribute, -Value)
% Print the prompt, read one term ending in '.', convert and validate it.
% Fails when the input runs out, which is how a run ends cleanly.
ask(Attr, Value) :-
    question(Attr, Prompt),
    write(Prompt),
    flush_output,
    safe_read(Raw),
    Raw \== end_of_file,
    echo_answer(Raw),
    convert(Attr, Raw, Converted),
    validate(Attr, Converted, Value).

% ask_all(+Attributes, -Values)
% Ask every question in order. Fails if any answer is missing.
ask_all([], []).
ask_all([Attr | Rest], [Value | Values]) :-
    ask(Attr, Value),
    ask_all(Rest, Values).


% =====================================================================
% SECTION 4 : WRITING THE RESULT
% =====================================================================

% result_line(+Disease, -Line)
% Builds the exact sentence required by the problem statement.
result_line(Disease, Line) :-
    disease_name(Disease, Name),
    format(atom(Line),
           'Result: The patient is likely suffering from: ~w', [Name]).

% reset_output
% Empty the output file so each run starts fresh. A file that cannot be
% opened (no permission, folder missing) is reported, not ignored.
reset_output :-
    output_file(File),
    catch(setup_call_cleanup(open(File, write, S), true, close(S)),
          Error,
          ( format('  [error] cannot open ~w for writing.~n', [File]),
            print_message(error, Error),
            fail )).

% append_output(+Line)
% Add one result line to the output file.
append_output(Line) :-
    output_file(File),
    catch(setup_call_cleanup(open(File, append, S),
                             format(S, '~w~n', [Line]),
                             close(S)),
          Error,
          ( format('  [error] cannot write to ~w.~n', [File]),
            print_message(error, Error) )).

% report(+Disease)
% Show the result on screen and store the same line in the output file.
report(Disease) :-
    result_line(Disease, Line),
    format('~w~n', [Line]),
    append_output(Line).


% =====================================================================
% SECTION 5 : DRIVER
% =====================================================================

% run_cases
% Diagnose one patient, then continue if there is more input.
run_cases :-
    input_left,
    attribute_order(Attrs),
    ask_all(Attrs, Values),
    !,
    Values = [F, C, P, R],
    diagnose(F, C, P, R, Disease),
    report(Disease),
    continue_cases.
run_cases.

% continue_cases
% From a file we go on to the next case, so one input file can hold
% several patients. On a terminal we stop after one patient, which is
% what the sample run shows.
continue_cases :-
    from_file,
    !,
    run_cases.
continue_cases.

% main
% Entry point: clear the output file, then process every case.
main :-
    reset_output,
    run_cases.


% =====================================================================
% SECTION 6 : TEST HELPERS  (commented out for submission)
% =====================================================================
% Runs the four attributes straight through the tree, skipping the
% prompts. Handy while developing; not used by the graded run.
%
% test(F, C, P, R) :-
%     diagnose(F, C, P, R, Disease),
%     disease_name(Disease, Name),
%     format('~w ~w ~w ~w -> ~w~n', [F, C, P, R, Name]).
%
% test_all :-
%     test(high_sudden, severe_dry, severe, absent),
%     test(high, none, excruciating, patchy),
%     test(101.9, persistent_dry, severe, absent),
%     test(none, mild, mild, absent).
