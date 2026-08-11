"""Generate the MIABS v0.1 one-page checklist PDF (reportlab/platypus)."""

import pathlib

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable)

INK = HexColor("#1a1a1a")
ACCENT = HexColor("#5a3d8a")
GREY = HexColor("#5c5c5c")

styles = getSampleStyleSheet()
title = ParagraphStyle("t", parent=styles["Title"], fontSize=16, leading=19,
                       textColor=INK, spaceAfter=1, alignment=0)
subtitle = ParagraphStyle("st", parent=styles["Normal"], fontSize=8.3,
                          leading=10.5, textColor=GREY, spaceAfter=4)
sec = ParagraphStyle("sec", parent=styles["Normal"], fontSize=8.8,
                     leading=10.5, textColor=ACCENT, spaceBefore=4,
                     spaceAfter=1.5, fontName="Helvetica-Bold")
item = ParagraphStyle("it", parent=styles["Normal"], fontSize=7.6,
                      leading=9.4, textColor=INK, leftIndent=12,
                      firstLineIndent=-12, spaceAfter=1.2)
foot = ParagraphStyle("f", parent=styles["Normal"], fontSize=7.0,
                      leading=8.8, textColor=GREY)


def I(code, text):
    return Paragraph(f'<font color="#5a3d8a"><b>{code}</b></font>&nbsp;&nbsp;{text}', item)


story = [
    Paragraph("MIABS v0.1: Minimum Information About a Behavioral Simulation", title),
    Paragraph("A reporting checklist for published simulations of operant and respondent processes. "
              "Every item asks authors to state information rather than to comply with a method. "
              "\u201cNot applicable\u201d is always acceptable; silence is not. "
              "Draft for public comment | CC-BY 4.0 | comments: [OSF project link]", subtitle),
    HRFlowable(width="100%", thickness=1.1, color=ACCENT, spaceAfter=3),

    Paragraph("A. Model specification", sec),
    I("A1", "State every equation or update rule governing the simulated organism, including auxiliary "
            "assumptions (response-emission mechanism, choice rule, noise model), not only the focal theoretical equation."),
    I("A2", "List every free parameter with permissible range, units, and interpretation; identify which are fitted, fixed, or derived."),
    I("A3", "Distinguish observables (rates, allocations, latencies, IRTs) from latent state variables "
            "(associative values, traces, activations); state which quantities predictions are expressed in."),
    I("A4", "State initial conditions for all state variables and how they were chosen."),

    Paragraph("B. Environment specification", sec),
    I("B1", "Specify each contingency completely: schedule type and parameters; interval-timer semantics "
            "(arranged vs. obtained; whether timers pause, reset, or run during reinforcement); reinforcer "
            "magnitude, duration, and delay; changeover requirements where applicable."),
    I("B2", "Specify stimulus conditions and their mapping to contingencies, including programmed "
            "stimulus\u2013consequence relations in respondent preparations (CS/US durations, ISI, ITI distributions)."),
    I("B3", "State session structure: length or termination criterion, number of sessions, and phase-transition criteria."),

    Paragraph("C. Temporal structure", sec),
    I("C1", "State whether time is continuous, discrete, or event-driven; if discrete, state the time step and "
            "report sensitivity of results to it."),
    I("C2", "State how simultaneous events are resolved (e.g., a response coinciding with a timer elapsing) "
            "and the order of operations within a step."),

    Paragraph("D. Stochasticity and reproducibility", sec),
    I("D1", "Identify every source of randomness in organism and environment, with distributions."),
    I("D2", "Report random seeds, number of simulated subjects/replicates, and how variability across replicates is summarized."),
    I("D3", "Provide runnable code and exact dependency versions sufficient to regenerate every figure, or state why not."),

    Paragraph("E. Parameterization and fitting", sec),
    I("E1", "State the objective function, fitting algorithm, convergence criteria, and starting-value strategy."),
    I("E2", "Report evidence that fitted parameters are recoverable: at minimum a parameter-recovery study; "
            "where model form permits, a structural identifiability analysis. Report any confounded or unidentifiable parameters."),
    I("E3", "If models are compared, state the comparison metric and how complexity is accounted for."),

    Paragraph("F. Validation scope", sec),
    I("F1", "List the phenomena the simulation is claimed to reproduce, with the qualitative signature of each "
            "(i.e., direction, ordering, or functional form, rather than merely \u201cmatches the data\u201d)."),
    I("F2", "State known boundary conditions: preparations, schedule ranges, or phenomena where the model is known or expected to fail."),
    I("F3", "Distinguish results the model was designed or tuned to produce from results that emerged without tuning."),

    Paragraph("G. Availability", sec),
    I("G1", "Deposit code, specification files, and generated data in a persistent repository with a DOI; state the license."),

    Spacer(1, 4),
    HRFlowable(width="100%", thickness=0.7, color=GREY, spaceAfter=2.5),
    Paragraph("Modeled on minimum-information standards in adjacent sciences (MIAME, 2001). Each item is "
              "included only because its omission has demonstrably produced a replication failure, hidden "
              "confound, or uninterpretable result; the evidence dossier accompanies this document. "
              "Version 0.1 | revised annually | [DOI]", foot),
]

doc = SimpleDocTemplate(str(pathlib.Path(__file__).resolve().parent / "MIABS_v0.1_onepager.pdf"),
                        pagesize=letter,
                        leftMargin=0.62 * inch, rightMargin=0.62 * inch,
                        topMargin=0.5 * inch, bottomMargin=0.45 * inch,
                        title="MIABS v0.1", author="MIABS Working Group (draft)")
doc.build(story)
print("built")
