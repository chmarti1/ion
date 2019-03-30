#include "ldisplay.h"       // For the display helper functions
#include "lgas.h"           // For gas measurements from the U12
#include <unistd.h>         


// Where should the columns be displayed on the screen?
#define COL1 25
#define COL2 60

#define CONFIG_FILE "monitor.conf"

double  flow_scfh,
        ratio_fto,
        oxygen_scfh,
        fuel_scfh;

/* INIT_DISPLAY
.   This prints the parameter text and headers to the screen.  The 
.   UPDATE_DISPLAY function will print the values that go with them.
*/
void init_display(void);


/* UPDATE_DISPLAY
.   Use the global variables to update the display values.  This function 
.   overwrites the old displayed data with new data.
*/
void update_display(void);



/********************************
 *                              *
 *          Algorithm           *
 *                              *
 ********************************/

int main(){
	double ftemp;

	LGAS_FG_OFFSET_SCFH = -.223;    

    init_display();
    while(1){
        // Get gas flow rates
        get_gas(&oxygen_scfh, &fuel_scfh);
        // Update the flow and ratio calculations
        flow_scfh = oxygen_scfh + fuel_scfh;
        ratio_fto = fuel_scfh / oxygen_scfh;

        // Finally, update the output values
        update_display();
    }
    return 0;
}


//*****************************************************************************
void init_display(void){
    clear_terminal();

    // Column 1: Temperature Measurements
    //  Plate temperature group
    print_header(2,1,"Flow and Mixture");
    print_bparam(3,COL1,"Total Flow (scfh)");
    print_bparam(4,COL1,"F/O Ratio");
    print_param(5,COL1,"Oxygen (scfh)");
    print_param(6,COL1,"Fuel (scfh)");

}

//*****************************************************************************
void update_display(void){

    // Column 1: Temperature Measurements
    //  Plate temperature group
    print_bflt(3,COL1,flow_scfh);
    print_bflt(4,COL1,ratio_fto);
    print_flt(5,COL1,oxygen_scfh);
    print_flt(6,COL1,fuel_scfh);

    LDISP_CGO(15,1);
    fflush(stdout);
}

