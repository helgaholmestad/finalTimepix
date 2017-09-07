*File{
*  Grid      = "@tdr@"
*  Plot      = "@tdrdat@"
*  Parameter = "@parameter@"
*  Current   = "@plot@"
*  Output    = "@log@"
*  Save	    = "n@node@_init"
*}

File{
  Grid      = "test1_msh.tdr"
  Plot      = "temp_results/2D-plots"
  Parameter = "sdevice.par"
  Current   = "temp_results/1D_plots"
  Output    = "log"
  Save	    = "init"
}

Electrode{
  { Name="PIX1"	Voltage=0.0 }
  { Name="PIX2"	Voltage=0.0 }
  { Name="PIX3"	Voltage=0.0 }
  { Name="PIX4" Voltage=0.0 }
  { Name="PIX5" Voltage=0.0 }
  { Name="PIX6"	Voltage=0.0 }
  { Name="PIX7"	Voltage=0.0 }
  { Name="PIX8"	Voltage=0.0 }
  { Name="PIX9" Voltage=0.0 }
  { Name="BACK"	Voltage=0.0 }
}

Physics{   
  EffectiveIntrinsicDensity( OldSlotboom )     
  Mobility(
    DopingDep
    HighFieldsaturation( GradQuasiFermi )
    Enormal
  )
  Recombination(
    SRH( DopingDep )
    *Avalanche( Eparallel )
  )
  Fermi
}

*Physics(MaterialInterface="Silicon/Oxide") {
*	Recombination(SurfaceSRH)
*	Traps(	(FixedCharge Conc=3e11)	)
*}

Plot{

  * eIonIntegral hIonIntegral MeanIonIntegral eAlphaAvalanche hAlphaAvalanche

  *--Density and Currents, etc
  eDensity hDensity
  TotalCurrent/Vector eCurrent/Vector hCurrent/Vector
  *--Fields and charges
  ElectricField/Vector Potential SpaceCharge
  
  *--Doping Profiles
  Doping 
  
  *--Generation/Recombination
  SRH * Band2Band Auger
  *SurfaceRecombination
  
  *AvalancheGeneration 
  *eAvalanche 
  *hAvalanche
  *eAvalancheGeneration 
  *hAvalancheGeneration
  
  *-- Lifetimes
  eLifeTime
  hLifeTime
}

Math {
  Cylindrical 
  Extrapolate
  Iterations=20
  Notdamped=100
  RelErrControl
  Method=ParDiSo
  Transient=BE
  Number_of_Threads=maximum
  CNormPrint

  *Avalderivatives
  ErRef(Electron)=1.e10
  ErRef(Hole)=1.e10   
}

Solve {
  *- Build-up of initial solution:
  Coupled(Iterations=100){ Poisson }
  Coupled { Poisson Electron Hole }
  
  Quasistationary(
    InitialStep=0.001 Increment=1.41 
    MinStep=1e-5 MaxStep=0.01
    Goal{ Name="BACK" Voltage=350 }
    Plot {Range = (0 1) Intervals=350}
  ) { Coupled { Poisson Electron Hole } }
}

