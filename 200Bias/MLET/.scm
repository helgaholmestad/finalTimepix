
;; Defined Parameters:

;; Contact Sets:
(sdegeo:define-contact-set "BACK" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX1" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX2" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX3" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX4" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX5" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX6" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX7" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX8" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "PIX9" 4 (color:rgb 1 0 0 )"##" )

;; Work Planes:
(sde:workplanes-init-scm-binding)

;; Defined ACIS Refinements:
(sde:refinement-init-scm-binding)

;; Reference/Evaluation Windows:
(sdedr:define-refeval-window "global_window" "Rectangle" (position 0 -1 0) (position 440 675 0))
(sdedr:define-refeval-window "back_doping_line" "Line" (position 3 675 0) (position 437 675 0))
(sdedr:define-refeval-window "pix1_doping_line" "Line" (position 0 0 0) (position 22.5 0 0))
(sdedr:define-refeval-window "pix2_doping_line" "Line" (position 32.5 0 0) (position 77.5 0 0))
(sdedr:define-refeval-window "pix3_doping_line" "Line" (position 87.5 0 0) (position 132.5 0 0))
(sdedr:define-refeval-window "pix4_doping_line" "Line" (position 142.5 0 0) (position 187.5 0 0))
(sdedr:define-refeval-window "pix5_doping_line" "Line" (position 197.5 0 0) (position 242.5 0 0))
(sdedr:define-refeval-window "pix6_doping_line" "Line" (position 252.5 0 0) (position 297.5 0 0))
(sdedr:define-refeval-window "pix7_doping_line" "Line" (position 307.5 0 0) (position 352.5 0 0))
(sdedr:define-refeval-window "pix8_doping_line" "Line" (position 362.5 0 0) (position 407.5 0 0))
(sdedr:define-refeval-window "pix9_doping_line" "Line" (position 418.5 0 0) (position 438 0 0))
(sdedr:define-refeval-window "particle1_window" "Rectangle" (position 0 0 0) (position 3 675 0))
(sdedr:define-refeval-window "particle2_window" "Rectangle" (position 3 0 0) (position 10 675 0))

;; Restore GUI session parameters:
(sde:set-window-position -9 47)
(sde:set-window-size 840 800)
(sde:set-window-style "Windows")
(sde:set-background-color 0 127 178 204 204 204)
(sde:scmwin-set-prefs "Liberation Sans" "Normal" 8 100 )
