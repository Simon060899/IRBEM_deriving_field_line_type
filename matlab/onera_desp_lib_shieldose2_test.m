% shieldose2_test - test shieldose2 function

%     1     1    70     2
Target = struct('material','Al','unit','g/cm2');
options = {'INUC',1,'NPTS',1001,'perYear',1};
Target.depth =  [0.000001 0.000002 0.000005 0.00001 0.00002 0.00005 0.0001 0.0002 0.0005 ...
   0.001  0.1  0.2  0.5  0.7  1.0  1.25  1.5  1.75  2.0  2.5 ...
   3.0   3.5   4.0   4.5   5.0   6.0   7.0   8.0   9.0  10.0 ...
  11.0  12.0  13.0  14.0  15.0  16.0  17.0  18.0  19.0  20.0 ...
  21.0  22.0  23.0  24.0  25.0  26.0  27.0  28.0  29.0  30.0 ...
  31.0  32.0  33.0  34.0  35.0  36.0  37.0  38.0  39.0  40.0 ...
  41.0  42.0  43.0  44.0  45.0  46.0  47.0  48.0  49.0  50.0 ...
  ];

%  0.100  10000.000  0.100  10000.000  1001  0.050  10.000  1001
% GEOSTAT,35790 KM,INCL=0,PLONG=160W; SP:1AL(95%),TP:NONE,EL:AEI7-HI(79)
%     3     0    28 1.00000E+03 3.15360E+07
SolSpect = struct('Erange',[0.1 1e4],'E0',2.65e+1,'N0',2.45e+10,'form','E');
% 0.0000E+00  0.0000E+00  0.0000E+00
%   2.6500E+01  2.4500E+10  0.0000E+00]';
SolSpect.N0 = SolSpect.N0/3.15360E+07; % convert to rate from fluence/duration
%SolSpect.N0 = SolSpect.N0*1e3; % convert /keV to /MeV (don't do this for exponential spectrum)
ProtSpect = [];
ElecSpect = [
  1.0000E-01  2.0000E-01  3.0000E-01  4.0000E-01  5.0000E-01  6.0000E-01 ...
  7.0000E-01  8.0000E-01  9.0000E-01  1.0000E+00  1.2500E+00  1.5000E+00 ...
  1.7500E+00  2.0000E+00  2.2500E+00  2.5000E+00  2.7500E+00  3.0000E+00 ...
  3.2500E+00  3.5000E+00  3.7500E+00  4.0000E+00  4.2500E+00  4.5000E+00 ...
  4.7500E+00  5.0000E+00  5.5000E+00  6.0000E+00
  7.5343E+04  5.7226E+04  3.5768E+04  2.0637E+04  1.2084E+04  7.7592E+03 ...
  5.3738E+03  4.0677E+03  3.3050E+03  2.0840E+03  9.4707E+02  4.4939E+02 ...
  2.2097E+02  1.0413E+02  5.1592E+01  2.6350E+01  1.2667E+01  5.7739E+00 ...
  2.9428E+00  1.8846E+00  1.4374E+00  1.1547E+00  8.4948E-01  6.2276E-01 ...
  4.8761E-01  3.4227E-01  2.1946E-01  1.2189E-02]';
ElecSpect(:,2) = ElecSpect(:,2)*1e3; % convert from /keV to /MeV
ElecSpect = struct('E',ElecSpect(:,1),'Flux',ElecSpect(:,2),'Erange',[0.05 10]);

[ProtDose,ElecDose,BremDose,SolDose,TotDose] = onera_desp_lib_shieldose2(ProtSpect,ElecSpect,SolSpect,Target,options{:});
loglog(Target.depth,TotDose,Target.depth,ProtDose+ElecDose+BremDose+SolDose,'k.');
xlabel(sprintf('Depth %s (%s)',Target.material,Target.unit));
ylabel('Dose (rads/year)');
legend('DOSE IN SEMI-INFINITE ALUMINUM MEDIUM',...
    'DOSE AT TRANSMISSION SURFACE OF FINITE ALUMINUM SLAB SHIELDS',...
    '1/2 DOSE AT CENTER OF ALUMINUM SPHERES',...
    'location','northoutside');

