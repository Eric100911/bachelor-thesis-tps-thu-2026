```latex
\chapter{Event Reconstruction and Selection}
\label{chap:reco-selection}

\section{Overview of the Analysis Strategy}
\label{sec:analysis-overview}

\section{Data and Simulated Samples}
\label{sec:samples}
  \subsection{Collision Data Samples}
  \label{subsec:data-samples}
  \subsection{Signal Monte Carlo Samples}
  \label{subsec:signal-mc}
  \subsection{Auxiliary Monte Carlo Samples}
  \label{subsec:auxiliary-mc}

\section{Primary Vertex and Track Reconstruction}
\label{sec:pv-track-reco}
  \subsection{Primary Vertex Reconstruction}
  \label{subsec:pv-reco}
  \subsection{Charged-Particle Track Reconstruction}
  \label{subsec:track-reco}
  \subsection{Track Quality Requirements}
  \label{subsec:track-quality}

\section{Muon Reconstruction and Selection}
\label{sec:muon-reco-selection}
  \subsection{Muon Reconstruction in CMS}
  \label{subsec:muon-reco}
  \subsection{Muon Kinematic Requirements}
  \label{subsec:muon-kinematic}
  \subsection{Muon Identification Requirements}
  \label{subsec:muon-id}

\section{\texorpdfstring{$J/\psi$}{J/psi} Candidate Reconstruction}
\label{sec:jpsi-reco}
  \subsection{Dimuon Pair Construction}
  \label{subsec:dimuon-construction}
  \subsection{Dimuon Vertex Fit}
  \label{subsec:dimuon-vertex-fit}
  \subsection{\texorpdfstring{$J/\psi$}{J/psi} Mass Window Selection}
  \label{subsec:jpsi-mass-window}

\section{\texorpdfstring{$\phi$}{phi} Candidate Reconstruction}
\label{sec:phi-reco}
  \subsection{Charged Kaon Candidate Selection}
  \label{subsec:kaon-selection}
  \subsection{Dikaon Pair Construction}
  \label{subsec:dikaon-construction}
  \subsection{\texorpdfstring{$\phi$}{phi} Mass Window Selection}
  \label{subsec:phi-mass-window}

\section{\texorpdfstring{$J/\psi J/\psi\phi$}{Jpsi Jpsi phi} Candidate Reconstruction}
\label{sec:triplet-reco}
  \subsection{Combination of Two \texorpdfstring{$J/\psi$}{J/psi} Candidates and One \texorpdfstring{$\phi$}{phi} Candidate}
  \label{subsec:triplet-combination}
  \subsection{Common-Vertex Requirement}
  \label{subsec:triplet-vertex}
  \subsection{Treatment of Multiple Candidates}
  \label{subsec:multiple-candidates}
  \subsection{Best-Candidate Selection}
  \label{subsec:best-candidate}

\section{Trigger and Event-Level Selection}
\label{sec:trigger-event-selection}
  \subsection{Trigger Paths}
  \label{subsec:trigger-paths}
  \subsection{Trigger Matching}
  \label{subsec:trigger-matching}
  \subsection{Event-Level Quality Requirements}
  \label{subsec:event-quality}

\section{Selected Candidate Sample}
\label{sec:selected-candidate-sample}
  \subsection{Summary of Selection Requirements}
  \label{subsec:selection-summary}
  \subsection{Candidate Yield after Selection}
  \label{subsec:selected-yield}
  \subsection{Mass Distributions before Signal Extraction}
  \label{subsec:prefit-mass-distributions}
```

```latex
\chapter{Signal Extraction and Efficiency Correction}
\label{chap:signal-efficiency}

\section{Overview}
\label{sec:signal-efficiency-overview}
  \subsection{From Reconstructed Candidates to Physics Results}
  \label{subsec:reco-to-physics}
  \subsection{Definition of the Raw and Corrected Signal Yields}
  \label{subsec:raw-corrected-yield-definition}

\section{Signal Extraction from the Three-Dimensional Mass Spectrum}
\label{sec:signal-extraction}
  \subsection{Fit Observables}
  \label{subsec:fit-observables}
  \subsection{Three-Dimensional Fit Strategy}
  \label{subsec:3d-fit-strategy}
  \subsection{Signal Model}
  \label{subsec:signal-model}
  \subsection{Background Model}
  \label{subsec:background-model}
  \subsection{Component Decomposition}
  \label{subsec:component-decomposition}
  \subsection{Fit Validation}
  \label{subsec:fit-validation}
  \subsection{Raw Signal Yield}
  \label{subsec:raw-signal-yield}
  \subsection{Signal Significance}
  \label{subsec:signal-significance}

\section{sPlot Method and Signal-Weighted Distributions}
\label{sec:splot}
  \subsection{Motivation for the sPlot Method}
  \label{subsec:splot-motivation}
  \subsection{Construction of Signal Weights}
  \label{subsec:sweight-construction}
  \subsection{Validation of sWeighted Distributions}
  \label{subsec:splot-validation}

\section{Acceptance Correction}
\label{sec:acceptance-correction}
  \subsection{Definition of the Fiducial Phase Space}
  \label{subsec:fiducial-phase-space}
  \subsection{Generator-Level Acceptance}
  \label{subsec:gen-acceptance}
  \subsection{Acceptance Maps}
  \label{subsec:acceptance-maps}

\section{Efficiency Correction}
\label{sec:efficiency-correction}
  \subsection{Factorization of the Total Efficiency}
  \label{subsec:efficiency-factorization}
  \subsection{Muon Reconstruction Efficiency}
  \label{subsec:muon-reco-efficiency}
  \subsection{Kaon Reconstruction Efficiency}
  \label{subsec:kaon-reco-efficiency}
  \subsection{Muon Identification Efficiency}
  \label{subsec:muon-id-efficiency}
  \subsection{Kaon Identification Efficiency}
  \label{subsec:kaon-id-efficiency}
  \subsection{Dimuon and Dikaon Reconstruction Efficiency}
  \label{subsec:dimuon-dikaon-efficiency}
  \subsection{Trigger Efficiency}
  \label{subsec:trigger-efficiency}
  \subsection{Four-Muon Vertexing Efficiency}
  \label{subsec:four-muon-vertexing-efficiency}
  \subsection{Triple-Candidate Vertexing and Event-Level Selection Efficiency}
  \label{subsec:triple-vertex-event-efficiency}

\section{Candidate Choice and Migration Effects}
\label{sec:candidate-choice-migration}
  \subsection{Origin of Candidate-Matching Ambiguities}
  \label{subsec:candidate-ambiguity-origin}
  \subsection{Generator-Level and Reconstruction-Level Candidate Definitions}
  \label{subsec:gen-reco-candidate-definition}
  \subsection{Migration Induced by Best-Candidate Selection}
  \label{subsec:best-candidate-migration}
  \subsection{Treatment in the Nominal Correction}
  \label{subsec:candchoice-nominal-treatment}

\section{Closure Tests}
\label{sec:closure-tests}
  \subsection{Inclusive Closure Test}
  \label{subsec:inclusive-closure-test}
  \subsection{Differential Closure Test}
  \label{subsec:differential-closure-test}
  \subsection{Closure Test for Candidate Choice}
  \label{subsec:candchoice-closure-test}
  \subsection{Residual Bias and Its Treatment}
  \label{subsec:closure-residual-bias}

\section{Efficiency-Corrected Signal Yield and Distributions}
\label{sec:corrected-results-method}
  \subsection{Event-by-Event Correction Formula}
  \label{subsec:event-by-event-correction}
  \subsection{Corrected Inclusive Signal Yield}
  \label{subsec:corrected-inclusive-yield}
  \subsection{Corrected Kinematic Distributions}
  \label{subsec:corrected-kinematic-distributions}

```

```latex
\chapter{Signal Extraction and Efficiency Correction}
\label{chap:signal-efficiency}

\section{Overview}
\label{sec:signal-efficiency-overview}
  \subsection{From Reconstructed Candidates to Physics Results}
  \label{subsec:reco-to-physics}
  \subsection{Definition of the Raw and Corrected Signal Yields}
  \label{subsec:raw-corrected-yield-definition}

\section{Signal Extraction from the Three-Dimensional Mass Spectrum}
\label{sec:signal-extraction}
  \subsection{Fit Observables}
  \label{subsec:fit-observables}
  \subsection{Three-Dimensional Fit Strategy}
  \label{subsec:3d-fit-strategy}
  \subsection{Signal Model}
  \label{subsec:signal-model}
  \subsection{Background Model}
  \label{subsec:background-model}
  \subsection{Component Decomposition}
  \label{subsec:component-decomposition}
  \subsection{Fit Validation}
  \label{subsec:fit-validation}
  \subsection{Raw Signal Yield}
  \label{subsec:raw-signal-yield}
  \subsection{Signal Significance}
  \label{subsec:signal-significance}

\section{sPlot Method and Signal-Weighted Distributions}
\label{sec:splot}
  \subsection{Motivation for the sPlot Method}
  \label{subsec:splot-motivation}
  \subsection{Construction of Signal Weights}
  \label{subsec:sweight-construction}
  \subsection{Validation of sWeighted Distributions}
  \label{subsec:splot-validation}

\section{Acceptance Correction}
\label{sec:acceptance-correction}
  \subsection{Definition of the Fiducial Phase Space}
  \label{subsec:fiducial-phase-space}
  \subsection{Generator-Level Acceptance}
  \label{subsec:gen-acceptance}
  \subsection{Acceptance Maps}
  \label{subsec:acceptance-maps}

\section{Efficiency Correction}
\label{sec:efficiency-correction}
  \subsection{Factorization of the Total Efficiency}
  \label{subsec:efficiency-factorization}
  \subsection{Muon Reconstruction Efficiency}
  \label{subsec:muon-reco-efficiency}
  \subsection{Kaon Reconstruction Efficiency}
  \label{subsec:kaon-reco-efficiency}
  \subsection{Muon Identification Efficiency}
  \label{subsec:muon-id-efficiency}
  \subsection{Kaon Identification Efficiency}
  \label{subsec:kaon-id-efficiency}
  \subsection{Dimuon and Dikaon Reconstruction Efficiency}
  \label{subsec:dimuon-dikaon-efficiency}
  \subsection{Trigger Efficiency}
  \label{subsec:trigger-efficiency}
  \subsection{Four-Muon Vertexing Efficiency}
  \label{subsec:four-muon-vertexing-efficiency}
  \subsection{Triple-Candidate Vertexing and Event-Level Selection Efficiency}
  \label{subsec:triple-vertex-event-efficiency}

\section{Candidate Choice and Migration Effects}
\label{sec:candidate-choice-migration}
  \subsection{Origin of Candidate-Matching Ambiguities}
  \label{subsec:candidate-ambiguity-origin}
  \subsection{Generator-Level and Reconstruction-Level Candidate Definitions}
  \label{subsec:gen-reco-candidate-definition}
  \subsection{Migration Induced by Best-Candidate Selection}
  \label{subsec:best-candidate-migration}
  \subsection{Treatment in the Nominal Correction}
  \label{subsec:candchoice-nominal-treatment}

\section{Closure Tests}
\label{sec:closure-tests}
  \subsection{Inclusive Closure Test}
  \label{subsec:inclusive-closure-test}
  \subsection{Differential Closure Test}
  \label{subsec:differential-closure-test}
  \subsection{Closure Test for Candidate Choice}
  \label{subsec:candchoice-closure-test}
  \subsection{Residual Bias and Its Treatment}
  \label{subsec:closure-residual-bias}

\section{Efficiency-Corrected Signal Yield and Distributions}
\label{sec:corrected-results-method}
  \subsection{Event-by-Event Correction Formula}
  \label{subsec:event-by-event-correction}
  \subsection{Corrected Inclusive Signal Yield}
  \label{subsec:corrected-inclusive-yield}
  \subsection{Corrected Kinematic Distributions}
  \label{subsec:corrected-kinematic-distributions}
```

```latex
\chapter{Systematic Uncertainties}
\label{chap:systematics}

\section{Overview}
\label{sec:syst-overview}
  \subsection{Classification of Uncertainty Sources}
  \label{subsec:syst-classification}
  \subsection{Propagation to Corrected Yields and Distributions}
  \label{subsec:syst-propagation}

\section{Uncertainties from Signal Extraction}
\label{sec:syst-signal-extraction}
  \subsection{Signal Mass Model}
  \label{subsec:syst-signal-model}
  \subsection{Background Mass Model}
  \label{subsec:syst-background-model}
  \subsection{Fixed Fit Parameters}
  \label{subsec:syst-fixed-parameters}
  \subsection{Fit Range}
  \label{subsec:syst-fit-range}
  \subsection{Fit Stability}
  \label{subsec:syst-fit-stability}
  \subsection{sPlot-Related Uncertainties}
  \label{subsec:syst-splot}

\section{Uncertainties from Acceptance and Efficiency Corrections}
\label{sec:syst-efficiency}
  \subsection{Monte Carlo Statistical Uncertainty}
  \label{subsec:syst-mc-stat}
  \subsection{Acceptance Map Binning}
  \label{subsec:syst-acceptance-binning}
  \subsection{Efficiency Map Binning}
  \label{subsec:syst-efficiency-binning}
  \subsection{Muon Reconstruction and Identification Efficiencies}
  \label{subsec:syst-muon-eff}
  \subsection{Kaon Reconstruction and Identification Efficiencies}
  \label{subsec:syst-kaon-eff}
  \subsection{Trigger Efficiency}
  \label{subsec:syst-trigger-eff}
  \subsection{Vertexing and Event-Level Selection Efficiencies}
  \label{subsec:syst-vertex-event-eff}

\section{Uncertainties from Candidate Reconstruction and Selection}
\label{sec:syst-candidate-selection}
  \subsection{Multiple-Candidate Treatment}
  \label{subsec:syst-multiple-candidates}
  \subsection{Best-Candidate Selection}
  \label{subsec:syst-best-candidate}
  \subsection{Candidate-Matching and Migration Effects}
  \label{subsec:syst-candidate-migration}
  \subsection{Closure-Test Residual Bias}
  \label{subsec:syst-closure-bias}

\section{Uncertainties from Sample Modeling}
\label{sec:syst-sample-modeling}
  \subsection{Signal Monte Carlo Modeling}
  \label{subsec:syst-signal-mc-modeling}
  \subsection{Kinematic Reweighting}
  \label{subsec:syst-kinematic-reweighting}
  \subsection{Model Dependence of Efficiency Corrections}
  \label{subsec:syst-model-dependence}
  \subsection{Pileup Modeling}
  \label{subsec:syst-pileup}

\section{Luminosity and Branching Fraction Uncertainties}
\label{sec:syst-normalization}
  \subsection{Integrated Luminosity}
  \label{subsec:syst-luminosity}
  \subsection{Branching Fractions}
  \label{subsec:syst-branching-fractions}

\section{Combination of Systematic Uncertainties}
\label{sec:syst-combination}
  \subsection{Correlation Assumptions}
  \label{subsec:syst-correlations}
  \subsection{Combination Procedure}
  \label{subsec:syst-combination-procedure}
  \subsection{Summary Table of Systematic Uncertainties}
  \label{subsec:syst-summary-table}
```