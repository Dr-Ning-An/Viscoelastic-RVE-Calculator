      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,
     1 RPL,DDSDDT,DRPLDE,DRPLDT,
     2 STRAN,DSTRAN,TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,CMNAME,
     3 NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,
     4 CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,JSTEP,KINC)
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME
      DIMENSION STRESS(NTENS),STATEV(NSTATV),
     1 DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),
     2 STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3),
     4 JSTEP(4)

      INTEGER nProny
      REAL*8 epsilonE(NTENS)
      REAL*8 C11_0,C12_0,C13_0,C22_0,C23_0,C33_0,C44_0,C55_0,C66_0
      REAL*8 C11i(1),C12i(1),C13i(1),C22i(1),C23i(1),C33i(1),C44i(1),C55i(1),C66i(1)
      REAL*8 tau1,tau2,tau3,tau4,tau5,tau6,tau7

! -----------------------------------------------------------
!     UMAT FOR 3D SOLID ELEMENTS
!     Developed by Ning An, May 2021.
! -----------------------------------------------------------

      IF (NDI.NE.3) THEN
         WRITE (7, *) 'THIS UMAT MAY ONLY BE USED FOR ELEMENTS
     1   WITH THREE DIRECT STRESS COMPONENTS'
         CALL XIT
      ENDIF

      C11_0     = PROPS(1)
      C11i(1)   = PROPS(2)
      C12_0     = PROPS(3)
      C12i(1)   = PROPS(4)
      C13_0     = C12_0 ! Symmetry
      C13i(1)   = C12i(1) ! Symmetry
      C22_0     = PROPS(5)
      C22i(1)   = PROPS(6)
      C33_0     = C22_0 ! Symmetry
      C33i(1)   = C22i(1) ! Symmetry
      C23_0     = PROPS(7)
      C23i(1)   = PROPS(8)
      C44_0     = PROPS(9)
      C44i(1)   = PROPS(10)
      C55_0     = PROPS(11)
      C55i(1)   = PROPS(12)
      C66_0     = C55_0
      C66i(1)   = C55i(1)

      tau1      = PROPS(13)

!     ELASTIC STIFFNESS

      DO K1=1,NTENS
        DO K2=1,NTENS
           DDSDDE(K1,K2)=0.0D0
        ENDDO
      ENDDO

      CurrTime = Time(2) + DTime

      DDSDDE(1,1) = C11_0 - C11i(1) * ( 1.0 - EXP(-CurrTime/tau1) ) 
      DDSDDE(1,2) = C12_0 - C12i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(1,3) = C13_0 - C13i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(2,2) = C22_0 - C22i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(2,3) = C23_0 - C23i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(3,3) = C33_0 - C33i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(4,4) = C66_0 - C66i(1) * ( 1.0 - EXP(-CurrTime/tau1) ) !     Abaqus notation
      DDSDDE(5,5) = C55_0 - C55i(1) * ( 1.0 - EXP(-CurrTime/tau1) )
      DDSDDE(6,6) = C44_0 - C44i(1) * ( 1.0 - EXP(-CurrTime/tau1) ) !     Abaqus notation

      DDSDDE(2,1) = DDSDDE(1,2)
      DDSDDE(3,1) = DDSDDE(1,3)
      DDSDDE(3,2) = DDSDDE(2,3)


!     CALCULATE STRESS 

      DO K=1,NTENS
        epsilonE(K) = STRAN(K)+DSTRAN(K)
      ENDDO

      DO K1=1,NTENS
        STRESS(K1)=0.0D0
        DO K2=1,NTENS
           STRESS(K1)=STRESS(K1)+DDSDDE(K1,K2)*(epsilonE(K2))
        ENDDO
      ENDDO

      RETURN
      END
