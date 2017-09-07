File{
  Grid      = "test1_msh.tdr"
  *--Plot      = "temp_results/2D-plots_PARTICLE"
  *--Plot      = "1keV/2D-plots_PARTICLE"
  Parameter = "sdevice.par"
  *--Current   = "temp_results/1D_plots_PARTICLE"
  Current   = "1keV/1D_plots_PARTICLE"
  Output    = "log2"
  *Save	    = "init"
}

Electrode{
  { Name="PIX1"	Voltage=0.0 }
  { Name="PIX2"	Voltage=0.0 }
  { Name="PIX3"	Voltage=0.0 }
  { Name="PIX4" Voltage=0.0 }
  { Name="PIX5" Voltage=0.0 }
 { Name="PIX6"	Voltage=0.0 }		
  { Name="PIX7" Voltage=0.0 }
  { Name="PIX8" Voltage=0.0 }
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
  
  HeavyIon (
  	  Direction=(0,1)
  	  Location=(0,337)
  	  Time=0
  	  Length=1
  	  Wt_hi=0.5
  	  LET_f=0.00004444444444
  	  Gaussian 
  	  PicoCoulomb )
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
  SRH *Band2Band Auger
  SurfaceRecombination
  
  AvalancheGeneration 
  eAvalanche 
  hAvalanche
  eAvalancheGeneration 
  hAvalancheGeneration
  
  *-- Lifetimes
  eLifeTime
  hLifeTime
  
  *--HeavyIon 
  HeavyIonChargeDensity
  HeavyIonGeneration
}

Math {
  Extrapolate
  Iterations=20
  Notdamped =100
  RelErrControl
  Method=ParDiSo
  Transient=BE
  Number_of_Threads=maximum

  RecBoxIntegr
  *Avalderivatives
  ErRef(Electron)=1.e10
  ErRef(Hole)=1.e10
}

Solve {
	load(Fileprefix="init_000200")
	Transient(
		InitialTime=0
		FinalTime=3e-6
		InitialStep=1e-12
		MinStep=1e-16
		MaxStep=100e-9
		Plot{Range=(0 3e-7) intervals=300}
		Plot{Range=(3e-7 3e-6) intervals=300}
		*--Plot{Range=(1e-7 3e-7) intervals=50}	
		*--Plot{Range=(5e-10 1e-9) intervals=50}
		*--Plot{Range=(1e-9 10e-9) intervals=50}
		*--Plot{Range=(10e-9 100e-9) intervals=5}
		*--Plot{Range=(100e-9 1e-6) intervals=5}
	){ Coupled{Poisson Electron Hole}
	CurrentPlot( 
	Time=(
		Range=(0 5e-12) intervals=50;
		Range=(5e-12 5e-11) intervals=50;		
		Range=(5e-11 5e-10) intervals=50;
		Range=(5e-10 5e-9) intervals=100;
		Range=(5e-9 1e-8) intervals=100;	
		Range=(1e-8 1e-7) intervals=100;
		Range=(1e-7 3e-6) intervals=300))
	}
	}

