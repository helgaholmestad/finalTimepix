Title ""

Controls {
}

Definitions {
	Constant "bulk_doping" {
		Species = "PhosphorusActiveConcentration"
		Value = 5e+11
	}
	AnalyticalProfile "nplus" {
		Species = "PhosphorusActiveConcentration"
		Function = Gauss(PeakPos = 0, PeakVal = 5e+19, ValueAtDepth = 1e+12, Depth = 2)
		LateralFunction = Gauss(Factor = 0.5)
	}
	AnalyticalProfile "pplus" {
		Species = "BoronActiveConcentration"
		Function = Gauss(PeakPos = 0, PeakVal = 5e+19, ValueAtDepth = 1e+12, Depth = 2)
		LateralFunction = Gauss(Factor = 0.5)
	}
	Refinement "global_refinement" {
		MaxElementSize = ( 10 10 0 )
		MinElementSize = ( 0.1 0.1 0 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
		RefineFunction = MaxLenInt(Interface("Silicon","SiO2"), Value=0.01, factor=1.4, DoubleSide)
	}
	Refinement "particle1_refinement" {
		MaxElementSize = ( 0.25 1 0 )
		MinElementSize = ( 0.25 1 0 )
	}
	Refinement "particle2_refinement" {
		MaxElementSize = ( 2 5 0 )
		MinElementSize = ( 2 5 0 )
	}
}

Placements {
	Constant "bulk_doping_placement" {
		Reference = "bulk_doping"
		EvaluateWindow {
			Element = Rectangle [(0 -1) (440 675)]
		}
	}
	AnalyticalProfile "back_side_doping_placement" {
		Reference = "nplus"
		ReferenceElement {
			Element = Line [(3 675) (437 675)]
		}
	}
	AnalyticalProfile "pix1_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(0 0) (22.5 0)]
		}
	}
	AnalyticalProfile "pix2_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(32.5 0) (77.5 0)]
		}
	}
	AnalyticalProfile "pix3_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(87.5 0) (132.5 0)]
		}
	}
	AnalyticalProfile "pix4_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(142.5 0) (187.5 0)]
		}
	}
	AnalyticalProfile "pix5_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(197.5 0) (242.5 0)]
		}
	}
	AnalyticalProfile "pix6_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(252.5 0) (297.5 0)]
		}
	}
	AnalyticalProfile "pix7_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(307.5 0) (352.5 0)]
		}
	}
	AnalyticalProfile "pix8_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(362.5 0) (407.5 0)]
		}
	}
	AnalyticalProfile "pix9_doping_placement" {
		Reference = "pplus"
		ReferenceElement {
			Element = Line [(418.5 0) (438 0)]
		}
	}
	Refinement "global_mesh_placement" {
		Reference = "global_refinement"
		RefineWindow = Rectangle [(0 -1) (440 675)]
	}
	Refinement "particle1_mesh_placement" {
		Reference = "particle1_refinement"
		RefineWindow = Rectangle [(0 0) (3 675)]
	}
	Refinement "particle2_mesh_placement" {
		Reference = "particle2_refinement"
		RefineWindow = Rectangle [(3 0) (10 675)]
	}
}

