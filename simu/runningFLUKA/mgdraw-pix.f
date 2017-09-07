
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
*
      DIMENSION DTQUEN ( MXTRCK, MAXQMG )
*
      CHARACTER*20 FILNAM
      character*9 regnam(4)
      LOGICAL LFCOPE, first
      SAVE LFCOPE, nctr,mctr,first,
     .       nSetup,nP0101,nP1616,nFake
      DATA LFCOPE /.FALSE./
      data first/.true./,
     .     regnam/'setup','p0101','p1616','fake'/
cc   ----------------
      integer idel
      save idel
      write(*,*) '--t-- new track'     
      write(*,*) '--t--',jtrack,xtrack(0),xtrack(1),ytrack(0),ytrack(1)
      write(*,*) '--t--',ztrack(0),ztrack(1)
 
      RETURN



      ENTRY BXDRAW(ic,mr,nr, x,y,z)
    
cc --- aug'14 04-01:00
cc     catch particles getting to / leaving tpx
cc
      j= jtrack
      ltrk= ltrack
      mtpx= -1
      !!write(*,*) 'beam crossing'
      !!write(*,*) nP0101,nP1616,nFake
      !!write(*,*) nr, mr
      !!write(*,*) jtrack
      if ((nr.ge.nP0101 .and. nr.le.nP1616) .or.
     .     (mr.ge.nP0101 .and. mr.le.nP1616)) then
        !!kommer vi her tilbake til cellenummeret vi egentlig er i. Vi far et tall mellom 1 256?. Altsa at det blir en intern nummerering av de 16times16 cellene i midten
        mtpx= (nr-P0101)/4 +1
        !!write (*,*) mtpx
        !!lt1trk initial lattice cell of the current track
        !!write (*,*) 'ltrk'
        !!write (*,*) ltrk
        l= lt1trk
        else
        mtpx= -1
        l= -1
        endif

      !!om vi er i 16times16gridet sa gar vi inn her
      if (mtpx.ge.0) then
        call tp(x,y,z,ix,iy,iz)
        !!write(*,*) 'konvertering'
        !!write (*,*) x,y,z,ix,iy,iz
        !!e er den totale energien til partikken
        e= -etrack
        !!energien blir satt til energien minus massen. Det vil si at e er kinetisk energi
        if (j.gt.-7) e= etrack-AM(j)
        !!write(*,2) mtpx,l,j,e, x,y,z, ix,iy,iz, ltrk,mr,nr

        !!her skal vi finne de partikkelene som gar inn i detektoren fra omrade fake. skjonner ikke helt. Det ser jo ut til at dette aldri skjer
        if (ltrack.eq.1) then
          if (mr.eq.nFake .and. nr.ge.nP0101 .and. nr.le.nP1616) then
             !!finner ikke ut hva cxtrck er for noe. Er dette relatert til vinkelen
            !!write(*,1) ncase,j,x,y,z,e, ix,iy,iz, CXTRCK,CYTRCK,CZTRCK
            endif
          endif
        endif
    2 format('  -b-   ',3i4,f16.9,'  ',3f9.4,'  ',3i5, 5i5)
    1 format('  -in-  ',2i7,3f9.4,f16.9,'  ',3i5,'  ',3f13.9)
      RETURN


      !!blir kalt pa slutten av et event
      ENTRY EEDRAW (ic)
      write(*,*) 'eedraw'
      !!write(*,*) ' -end- ',ncase
      call fflush()
      RETURN


      !!blir kalt for hvert lokale energitap. Hva menes egentlig med et lokalt energitap. Er det noen energitap som ikke blir tatt med her
      ENTRY ENDRAW(ic,mr, RULL, x,y,z)
      write(*,*) 'endraw'
      !!RULL= hvor mye energi er deponert
      j= jtrack
      if (idel.gt.0) then
         !!vi er bare interessert i elektroner og elektromagnetiske prosesser
         if (j.eq.3 .and. ic.gt.20) then
          !!if (idel.gt.1) write(*,*) ' -ee- ',ncase,ic,idel,rull
          if (idel.eq.1) then
            call tp(x,y,z, ix,iy,iz)
            !!write(*,5) ic,idel,rull, x,y,z, ix,iy,iz
            endif
          idel= idel-1
          endif
        endif
    5 format('  -e- ',2i3,f16.9,'  ',3f9.4,'  ',3i5)
      RETURN


     !!blir kalt hver gang en partikkel kildepartikkel starter, det vil si pa begynnelsen av eventet. 
      ENTRY SODRAW
      write(*,*) '--t--',' begin'
cc   -----------------
      !!Dette gjor vi kun for forste eventet
      if (first) then
        first= .false.
cc     ---------------------------------------- idenify region indeces
        call GEON2R(regnam(1),nSetup,ierr)
        call GEON2R(regnam(2),nP0101,ierr)
        call GEON2R(regnam(3),nP1616,ierr)
        call GEON2R(regnam(4),nFake,ierr)

        !!write(*,*)  ' -s- ',nSetup,nP0101,nP1616,nG0101,nG1616
        endif

      !!wtflk particle statistical weight
      w= Wtflk(1)
      !!ek particle labratory kinetic energyt
      ek= TKEFLK(1)
      !!ncase current number of beam particles followed, tror det bli eventnummeret
      !!ILOFLK particle identity
      !! *flk posisjonen til partikkelen
      !!write(*,3) ncase,ILOFLK(1),ek, xflk(1),yflk(1),zflk(1)

      idel= 0
    3 format('  -evt- ',i7,i7,' -- ',f16.9,3f9.4)
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
*  tron is present ad stacked on FLKSTK common for kp=npflka          *
*                                                                      *
*======================================================================*

      !!blir kalt hver gang det skjer en intraksjon
      ENTRY USDRAW(ic,mr, x,y,z)
      !!write(*,*) 'usdraw'
      !!write(*,*) jtrack
      !!write(*,*) x,y,z
      !!write(*,*) 'her',ntrack
      !!write(*,*) xtrack(2)


cc   ----------------------------
      !!ser ut til at vi her teller opp diverse elektronprosesser. Men hvorfor ma vi ha delta ray generation for vi i det hele tatt kan plukke opp de andre prosessene. 
      j= jtrack
      !!skjekker om vi er inni det interessante omradet
      if (mr.ge.nP0101 .and. mr.le.nP1616) then
         !!finner pixelen inni dette omradet. Hvorfor bestar dette omradet av 1020 regioner. hvorfor bare delt i 4 i tillegg til de 16 pixlene??
         mtpx= (mr-P0101)/4 +1
        else
        mtpx= -1
        endif

        if (idel.gt.0) then
           if (ic.eq.210 .or. ic.eq.211 .or. ic.eq.219) then
              idel= idel+1
              !!write(*,*) ' -u- +++ ',ncase,ic,mr,ic,idel,mtpx,lt1trk
           endif
        endif

 !!ic=103 betyr delta ray generation secondaries (hva i alle dager betyr det). Tror det betyr at vi har et elektron som blir produsert og har nok energi til a komme seg bort fra stedet der det ble laget
        if (mtpx.ge.0 .and. ic.eq.103) then
           e= etrack-AM(j)
           ek= tki(2)
           idel= idel+1
           call tp(x,y,z, ix,iy,iz)
           !!write(*,4) idel, ek, x,y,z, ix,iy,iz, mtpx,lt1trk
           
        endif

 4      format('  -u-    ',i3,f16.9,'  ',3f9.4,'  ',3i5, '  - ',4i5)
        END


cc
cc
cc

      subroutine tp(x,y,z, ix,iy,iz)
cc   --------------------------------
      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'

      save w,dw,ow, dcell
      data dw/.0055/,w/1.408/,ow/-.704/,dcell/.0005/

      !!her konverteres det til et grid med bokser pa 5 micron
      ix= (x-ow)/dcell
      iy= (y-ow)/dcell
      iz= z/dcell

      end

