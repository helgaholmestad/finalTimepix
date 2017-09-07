
cc
cc --- aug'14 04-01:00
cc
cc     timepix, companion to EVENTBIN - try to prepare a charge cloud
cc

      SUBROUTINE MGDRAW(ic,mr)

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'

*     Copyright (C) 1990-2006      by        Alfredo Ferrari           *
*     All Rights Reserved.                                             *
*     MaGnetic field trajectory DRAWing: actually this entry manages   *
*                                        all trajectory dumping for    *
*                                        drawing                       *
*     Created on   01 march 1990   by        Alfredo Ferrari           *
*                                              INFN - Milan            *
*     Last change  05-may-06       by        Alfredo Ferrari           *
*                                              INFN - Milan            *

      INCLUDE '(CASLIM)'
      INCLUDE '(COMPUT)'
      INCLUDE '(SOURCM)'
      INCLUDE '(FHEAVY)'
      INCLUDE '(FLKSTK)'
      INCLUDE '(GENSTK)'
      INCLUDE '(MGDDCM)'
      INCLUDE '(PAPROP)'
      INCLUDE '(QUEMGD)'
      INCLUDE '(SUMCOU)'
      INCLUDE '(TRACKR)'
      INCLUDE '(DPDXCM)'
*
*
      DIMENSION DTQUEN ( MXTRCK, MAXQMG )
*
cc   ----------------
      integer idel
      save idel

      RETURN


      ENTRY BXDRAW(ic,mr,nr, x,y,z)
      RETURN


      ENTRY EEDRAW (ic)
      call fflush()
      RETURN


      ENTRY ENDRAW(ic,mr, RULL, x,y,z)
      RETURN


      ENTRY SODRAW
cc   -----------------
      RETURN




*======================================================================*
*                                                                      *
*     USer dependent DRAWing:                                          *
*                                                                      *
*     Icode = 10x: call from Kaskad                                    *
*             100: elastic   interaction secondaries                   *
*             101: inelastic interaction secondaries                   *
*             102: particle decay  secondaries                         *
*             103: delta ray  generation secondaries                   *
*             104: pair production secondaries                         *
*             105: bremsstrahlung  secondaries                         *
*             110: decay products                                      *
*     Icode = 20x: call from Emfsco                                    *
*             208: bremsstrahlung secondaries                          *
*             210: Moller secondaries                                  *
*             212: Bhabha secondaries                                  *
*             214: in-flight annihilation secondaries                  *
*             215: annihilation at rest   secondaries                  *
*             217: pair production        secondaries                  *
*             219: Compton scattering     secondaries                  *
*             221: photoelectric          secondaries                  *
*             225: Rayleigh scattering    secondaries                  *
*     Icode = 30x: call from Kasneu                                    *
*             300: interaction secondaries                             *
*     Icode = 40x: call from Kashea                                    *
*             400: delta ray  generation secondaries                   *
*  For all interactions secondaries are put on GENSTK common (kp=1,np) *
*  but for KASHEA delta ray generation where only the secondary elec-  *
*  tron is present and stacked on FLKSTK common for kp=npflka          *
*                                                                      *
*======================================================================*

      ENTRY USDRAW(ic,mr, x,y,z)
cc   ----------------------------
      j=jtrack
   
c$$$      
c$$$      denne funksjonen blir kalt etter hver intraksjon
c$$$      ncase=number of primaries treathed so far
c$$$      mr =current region
c$$$      x,y,z interaction point
c$$$      jtrack = type of particle
c$$$          npheav = number of heavy secondarie
c$$$          np = number of secondaries
c$$$          kpart??

          
!hvis partikkelen er anti-proton og intraksjonen er inelastisk (det vil si kinetisk energi ikke er konservert) 
          if (j.eq.2 .and. ic.eq.101) then
             write(*,*) 'Kun en gang per event'
             write(*,*) ' o ',ncase,mr,x,y,z, NP,NPHEAV
             do i=1,NP
                write(*,*) ' oo ',kpart(i),tki(i)*1000             
             enddo
             if (npheav.gt.0) then
                do j=1,npheav,1
                   write(*,*) ' -h- ',kheavy(j),tkheav(j)*1000
                end do
                !!write(*,*) ' -h- ',npheav,((kheavy(j),tkheavy(j)),j=1,npheav)
               !! write(*,*) ' -e- ',npheav,(tkheavy(j),j=1,npheav)
             endif
          endif
          
          END


