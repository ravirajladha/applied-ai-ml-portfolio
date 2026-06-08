# Applied AI/ML Coursework Portfolio

Personal archive of notes, lab notebooks, slides, and webinar material from my
ongoing M.Tech journey — mirrors the subject/session structure used on the
Taxila LMS. Heavy PDFs are kept on Drive and linked from each subject's
`resources.md` rather than committed (see `.gitignore`).

Large binary files (`.pptx`, `.xlsx`) are tracked with [Git LFS](https://git-lfs.com/).

## Subjects

| Subject | Folder |
| --- | --- |
| Software Engineering for Machine Learning | [`software-engineering-for-machine-learning/`](software-engineering-for-machine-learning/) |
| Artificial and Computational Intelligence | [`artificial-and-computational-intelligence/`](artificial-and-computational-intelligence/) |
| Deep Reinforcement Learning | [`deep-reinforcement-learning/`](deep-reinforcement-learning/) |
| Natural Language Processing | [`natural-language-processing/`](natural-language-processing/) |

More subjects will be added as the semester progresses. See [`GUIDE.md`](GUIDE.md)
for folder conventions, the Git LFS/secrets setup, and how to add a new subject.

## Layout

Each subject folder follows the same structure:

```
<subject>/
├── notes.md        # running notes for the subject
├── resources.md    # links to slides/readings/PDFs hosted on Drive
├── materials/      # slides and other course material (.pptx tracked via LFS)
└── webinars/       # webinar notebooks (.ipynb) and accompanying data (.xlsx)
```
