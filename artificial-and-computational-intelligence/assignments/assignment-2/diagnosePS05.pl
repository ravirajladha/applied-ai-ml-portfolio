% =====================================================================
%  Assignment 2 - PS05 : Disease Diagnosis from a Decision Tree
%  Course  : AIMLCZG557 / AECLZG557  (S2 2025-2026)
%  Group   : G000
%  Engine  : SWI-Prolog
%
%  Predicts Influenza / COVID-19 / Dengue / Common Cold from four
%  symptom values, by walking the decision tree given in the problem.
%
%  How to run
%    Interactive : swipl diagnosePS05.pl
%                  ?- diagnose.
%    Batch       : swipl -q -g diagnose -t halt diagnosePS05.pl
%                        < inputPS05.txt > outputPS05.txt
%
%  Sections
%    1. Knowledge base   - allowed symptom values and prompt texts
%    2. Node tests       - raw answers -> decision tree branch labels
%    3. Decision tree    - one clause per root-to-leaf path
%    4. Input            - prompt, read, validate, re-ask on error
%    5. Output           - the result line
%    6. Main             - diagnose/0
% =====================================================================


% ---------------------------------------------------------------------
% 1. KNOWLEDGE BASE
% ---------------------------------------------------------------------

% symptom(Order, Name) - the four questions, asked in this order.
symptom(1, fever).
symptom(2, cough).
symptom(3, pain).
symptom(4, rash).

% valid(Symptom, AllowedValues) - anything else is rejected.
valid(fever, [high_sudden, high, mild, none]).
valid(cough, [severe_dry, persistent_dry, mild, none]).
valid(pain,  [severe, excruciating, mild, none]).
valid(rash,  [absent, patchy]).

% prompt(Symptom, Text) - wording fixed by the problem statement.
prompt(fever, 'Is the Fever Intensity (high_sudden/high/mild/none)? ').
prompt(cough, 'Is the Cough Type (severe_dry/persistent_dry/mild/none)? ').
prompt(pain,  'Is the Body Pain Severity (severe/excruciating/mild/none)? ').
prompt(rash,  'Is the Skin Rash Type (absent/patchy)? ').


% ---------------------------------------------------------------------
% 2. NODE TESTS
%    Each predicate here is one yes/no question in the tree diagram.
% ---------------------------------------------------------------------

% Node 1 - "Is Fever >= 100.4 F (High)?"
% Both high grades sit above the threshold; mild/none sit below it.
high_fever(high_sudden).
high_fever(high).

% Node 2 - "Is there a Skin Rash?"
% Only the flat, red, patchy rash counts (the Dengue marker).
skin_rash(patchy).

% Node 3 - "How bad is Body Pain & Cough severity?"
severe_pain(severe).
severe_pain(excruciating).

hacking_cough(severe_dry).
hacking_cough(persistent_dry).

dry_cough(severe_dry).
dry_cough(persistent_dry).
dry_cough(mild).

% Node 4 - "Is Taste/Smell Lost?"
% Loss of taste/smell is not one of the four inputs, so it is derived
% from the severity matrix: a persistent dry cough is the COVID-19
% signature, while a severe hacking cough points away from it.
taste_smell_lost(persistent_dry).

% Low fever node - "Are Cough/Sore Throat Mild & Body Aches Mild?"
mild_symptom(mild).
mild_symptom(none).


% ---------------------------------------------------------------------
% 3. DECISION TREE
%    diagnosis(Fever, Cough, Pain, Rash, Disease)
%    Clauses are tried top to bottom, so their order mirrors the
%    diagram. The cut in each clause fixes the branch once taken.
% ---------------------------------------------------------------------

% --- High fever path -------------------------------------------------

% Patchy rash ends the walk immediately.
diagnosis(F, _, _, R, 'Dengue') :-
    high_fever(F),
    skin_rash(R), !.

% Severe body pain + hacking cough.
diagnosis(F, C, P, _, D) :-
    high_fever(F),
    severe_pain(P),
    hacking_cough(C), !,
    (   taste_smell_lost(C)
    ->  D = 'COVID-19'
    ;   D = 'Influenza'
    ).

% Moderate body pain + dry cough.
diagnosis(F, C, P, _, D) :-
    high_fever(F),
    \+ severe_pain(P),
    dry_cough(C), !,
    (   taste_smell_lost(C)
    ->  D = 'COVID-19'
    ;   D = 'Other Virus'
    ).

% High fever that matches neither branch above.
diagnosis(F, _, _, _, 'Other Virus') :-
    high_fever(F), !.

% --- Low / mild fever path -------------------------------------------

% Mild cough and mild body aches.
diagnosis(_, C, P, _, 'Common Cold') :-
    mild_symptom(C),
    mild_symptom(P), !.

% Everything else on this path.
diagnosis(_, _, _, _, 'Allergies or Other Infection').


% ---------------------------------------------------------------------
% 4. INPUT
% ---------------------------------------------------------------------

% ask(+Symptom, -Value) - prompt, read one term, validate it.
ask(Symptom, Value) :-
    prompt(Symptom, Text),
    valid(Symptom, Allowed),
    write(Text),
    read_answer(Answer),
    check(Symptom, Answer, Allowed, Value).

% read_answer(-Term) - a malformed term becomes 'invalid_input' instead
% of crashing the program.
read_answer(Answer) :-
    catch(read(user_input, Answer), _, Answer = invalid_input).

% check(+Symptom, +Answer, +Allowed, -Value)
% Input ran out before all four symptoms were given.
check(_, end_of_file, _, _) :-
    !,
    nl,
    write('Error: input ended before all four symptoms were given.'), nl,
    fail.
% Answer is in the allowed list - accept it.
check(_, Answer, Allowed, Answer) :-
    memberchk(Answer, Allowed), !,
    echo(Answer).
% Anything else - report and ask the same question again.
check(Symptom, Answer, Allowed, Value) :-
    echo(Answer),
    format('Error: "~w" is not a valid value. Expected one of ~w.~n',
           [Answer, Allowed]),
    ask(Symptom, Value).

% echo(+Answer) - when input comes from a file the answer is not shown
% on screen, so print it; a terminal already echoes what was typed.
echo(Answer) :-
    (   stream_property(user_input, tty(true))
    ->  true
    ;   format('~w.~n', [Answer])
    ).


% ---------------------------------------------------------------------
% 5. OUTPUT
% ---------------------------------------------------------------------

report(Disease) :-
    format('Result: The patient is likely suffering from: ~w~n', [Disease]).


% ---------------------------------------------------------------------
% 6. MAIN
% ---------------------------------------------------------------------

% diagnose/0 - ask the four questions, walk the tree, print the result.
diagnose :-
    (   ask(fever, F),
        ask(cough, C),
        ask(pain,  P),
        ask(rash,  R)
    ->  diagnosis(F, C, P, R, Disease),
        report(Disease)
    ;   write('Result: no diagnosis - incomplete symptom data.'), nl
    ).


% ---------------------------------------------------------------------
% Test helper - commented out for submission, as per the instructions.
%
% show_tree/0 lists every combination of symptom values with the
% disease the tree predicts for it. Used while developing to confirm
% that all leaves are reachable and no combination is left unmatched.
%
% show_tree :-
%     valid(fever, Fs), valid(cough, Cs),
%     valid(pain,  Ps), valid(rash,  Rs),
%     forall(( member(F, Fs), member(C, Cs),
%              member(P, Ps), member(R, Rs) ),
%            ( diagnosis(F, C, P, R, D),
%              format('~w ~w ~w ~w -> ~w~n', [F, C, P, R, D]) )).
% ---------------------------------------------------------------------
