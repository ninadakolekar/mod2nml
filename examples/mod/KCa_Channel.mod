COMMENT
    A channel from Maex, R and De Schutter, E. Synchronization of Golgi and Granule Cell Firing in a 
    Detailed Network Model of the Cerebellar Granule Cell Layer
ENDCOMMENT

TITLE Channel: Gran_KCa_98

COMMENT
    Calcium concentration dependent K+ channel
ENDCOMMENT


UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}


    
NEURON {
  
    SUFFIX Gran_KCa_98
    USEION k READ ek WRITE ik VALENCE 1 ? reversal potential of ion is read, outgoing current is written
           
        
    USEION ca READ cai VALENCE 2 ? internal concentration of ion is read

    
    RANGE gmax, gion
    
    RANGE minf, mtau
    
}

PARAMETER { 
  
    gmax = 0.0000179811 (S/cm2) ? default value, should be overwritten when conductance placed on cell
    
}



ASSIGNED {
  
    v (mV)
    
    celsius (degC)
      
    ? Reversal potential of k
    ek (mV)
    ? The outward flow of ion: k calculated by rate equations...
    ik (mA/cm2)
      
    ? The internal concentration of ion: ca is used in the rate equations...
    cai (mM) 
    
    
    gion (S/cm2)
    minf
    mtau (ms)
    
}

BREAKPOINT { 
    SOLVE states METHOD derivimplicit
    gion = gmax * (m^1) 
    ik = gion*(v - ek)
            

}



INITIAL {
    
    ek = -90
        
    settables(v,cai)
    m = minf
        
    
}
    
STATE {
    m
    
}



DERIVATIVE states {
    settables(v,cai)
    m' = (minf - m)/mtau
            

}

PROCEDURE settables(v(mV), cai(mM)) { 
    
    ? Note: not all of these may be used, depending on the form of rate equations
    LOCAL alpha, beta, tau, inf, gamma, zeta, ca_conc, temp_adj_m
    
    UNITSOFF
    
    ? There is a Q10 factor which will alter the tau of the gates 
             
    temp_adj_m = 3^((celsius - 17.350264793)/10)
    
    ? There is a voltage offset of 0.010. This will shift the dependency of the rate equations 
    v = v - (10)
    
    ? Gate depends on the concentration of ca
    ca_conc = cai ? In NEURON, the variable for the concentration of ca is cai
    
            
                
       
        
    ? *** Adding rate equations for gate: m ***
         
    ? Found a generic form of the rate equation for alpha, using expression: 2500/(1 + ( (1.5e-3 *(exp (-85*v))) / ca_conc))
    
    ? Note: Equation (and all ChannelML file values) in SI Units so need to convert v first...
    
    v = v * 0.001 ? temporarily set v to units of equation...
            
    alpha = 2500/(1 + ( (1.5e-3 *(exp (-85*v))) / ca_conc))
        
    ? Set correct units of alpha for NEURON
    alpha = alpha * 0.001 
    
    v = v * 1000 ? reset v
        
     
    ? Found a generic form of the rate equation for beta, using expression: 1500/(1 + (ca_conc / (1.5e-4 * (exp (-77*v)))))
    
    ? Note: Equation (and all ChannelML file values) in SI Units so need to convert v first...
    
    v = v * 0.001 ? temporarily set v to units of equation...
            
    beta = 1500/(1 + (ca_conc / (1.5e-4 * (exp (-77*v)))))
        
    ? Set correct units of beta for NEURON
    beta = beta * 0.001 
    
    v = v * 1000 ? reset v
        
    mtau = 1/(temp_adj_m*(alpha + beta))
    minf = alpha/(alpha + beta)
    


    ? *** Finished rate equations for gate: m ***
    

     
}


UNITSON
