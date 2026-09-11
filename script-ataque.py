Durante o ataque 

set routing-options static route 138.185.108.0/24 community 65000:6666
set routing-options static route 138.185.109.0/24 community 65000:6666
set routing-options static route 138.185.110.0/24 community 65000:6666
set routing-options static route 138.185.111.0/24 community 65000:6666

set routing-options static route 170.246.96.0/24 community 65000:6666
set routing-options static route 170.246.97.0/24 community 65000:6666
set routing-options static route 170.246.98.0/24 community 65000:6666
set routing-options static route 170.246.99.0/24 community 65000:6666

set routing-options static route 177.84.108.0/24 community 65000:6666
set routing-options static route 177.84.109.0/24 community 65000:6666
set routing-options static route 177.84.110.0/24 community 65000:6666
set routing-options static route 177.84.111.0/24 community 65000:6666

ASN 264088
set routing-options static route 138.94.80.0/24 community 65000:6666
set routing-options static route 138.94.81.0/24 community 65000:6666
set routing-options static route 138.94.82.0/24 community 65000:6666
set routing-options static route 138.94.83.0/24 community 65000:6666


set routing-options static route 143.208.4.0/24 community 65000:6666
set routing-options static route 143.208.5.0/24 community 65000:6666
set routing-options static route 143.208.6.0/24 community 65000:6666


pmj router de palmas
active policy-options policy-statement ibgp-export term ataque-provisorio
143.208.7.0/24 esta em palmas


=====================================================================================
remover o ataque

delete routing-options static route 138.185.108.0/24 community 65000:6666
delete routing-options static route 138.185.109.0/24 community 65000:6666
delete routing-options static route 138.185.110.0/24 community 65000:6666
delete routing-options static route 138.185.111.0/24 community 65000:6666

delete routing-options static route 170.246.96.0/24 community 65000:6666
delete routing-options static route 170.246.97.0/24 community 65000:6666
delete routing-options static route 170.246.98.0/24 community 65000:6666
delete routing-options static route 170.246.99.0/24 community 65000:6666

delete routing-options static route 177.84.108.0/24 community 65000:6666
delete routing-options static route 177.84.109.0/24 community 65000:6666
delete routing-options static route 177.84.110.0/24 community 65000:6666
delete routing-options static route 177.84.111.0/24 community 65000:6666

delete routing-options static route 138.94.80.0/24 community 65000:6666
delete routing-options static route 138.94.81.0/24 community 65000:6666
delete routing-options static route 138.94.82.0/24 community 65000:6666
delete routing-options static route 138.94.83.0/24 community 65000:6666




set routing-options static route 138.185.108.0/22 community 52721:11
set routing-options static route 138.185.108.0/23 community 52721:12
set routing-options static route 138.185.108.0/24 community 52721:13
set routing-options static route 138.185.109.0/24 community 52721:13
set routing-options static route 138.185.110.0/23 community 52721:12
set routing-options static route 138.185.110.0/24 community 52721:13
set routing-options static route 138.185.111.0/24 community 52721:13



set routing-options static route 170.246.96.0/22 community 52721:11
set routing-options static route 170.246.96.0/23 community 52721:12
set routing-options static route 170.246.96.0/24 community 52721:13
set routing-options static route 170.246.97.0/24 community 52721:13
set routing-options static route 170.246.98.0/23 community 52721:12
set routing-options static route 170.246.98.0/24 community 52721:13
set routing-options static route 170.246.99.0/24 community 52721:13



set routing-options static route 177.84.108.0/22 community 52721:11
set routing-options static route 177.84.108.0/23 community 52721:12
set routing-options static route 177.84.108.0/24 community 52721:13
set routing-options static route 177.84.109.0/24 community 52721:13
set routing-options static route 177.84.110.0/23 community 52721:12
set routing-options static route 177.84.110.0/24 community 52721:13
set routing-options static route 177.84.111.0/24 community 52721:13



set routing-options static route 143.208.4.0/22 community 52721:11
set routing-options static route 143.208.4.0/23 community 52721:12
set routing-options static route 143.208.4.0/24 community 52721:13
set routing-options static route 143.208.5.0/24 community 52721:13
set routing-options static route 143.208.6.0/23 community 52721:12
set routing-options static route 143.208.6.0/24 community 52721:13




/configure router bgp  group "transit-ipv4" 
shutdown
/configure router bgp  group "peering-ixbr-sp4-ipv4" 
shutdown



/configure router bgp  group "transit-ipv4" 
shutdown
/configure router bgp group "peering-ixbr-for1-ipv4" 
shutdown

