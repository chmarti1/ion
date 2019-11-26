/*MON
 * This executable monitors the experimental conditions for the wire
 * copter experiment.
 */

#include "lconfig/lconfig.h"
#include "lconfig/lctools.h"
#include <stdio.h>

#define MON_CONF "monitor.conf"
#define MON_GASDEV	0
#define MON_RPMDEV 	1
#define MON_COLUMN	20
#define MON_RPM_ROW	2
#define MON_O2_ROW 5
#define MON_FG_ROW 6
#define MON_FLOW_ROW 7
#define MON_FTO_ROW 8
#define MON_MSG_ROW 9
#define MON_FG_CHANNEL 0
#define MON_O2_CHANNEL 1

#define halt(){\
	lct_finish_keypress();\
	lc_stream_stop(&dconf[MON_GASDEV]);\
	lc_close(&dconf[MON_GASDEV]);\
	lc_close(&dconf[MON_RPMDEV]);\
	return -1;\
}

int main(){
	lc_devconf_t dconf[2];
	double values[2], o2, fg;
	int err, channels, samples_per_read;
	char go_f;
	
	// Load the configuration and open a connection to the labjacks
	if (	lc_load_config(dconf, 2, MON_CONF) ||
			lc_open(&dconf[MON_GASDEV]) ||
			lc_upload_config(&dconf[MON_GASDEV]) ||
			lc_open(&dconf[MON_RPMDEV]) ||
			lc_upload_config(&dconf[MON_RPMDEV])){
		fprintf(stderr, "Failed to open device donnections\n");
		halt();
	}
	
	//lc_show_config(&dconf[MON_GASDEV]);
	//lc_show_config(&dconf[MON_RPMDEV]);
	

	// Initialize the screen
	lct_clear_terminal();
	lct_print_param(MON_RPM_ROW, MON_COLUMN, "Disc speed (Hz)");
	lct_print_param(MON_RPM_ROW+1, MON_COLUMN, "(RPM)");
	lct_print_param(MON_O2_ROW, MON_COLUMN, "O2 Flow (scfh)");
	lct_print_param(MON_FG_ROW, MON_COLUMN, "FG Flow (scfh)");
	lct_print_param(MON_FLOW_ROW, MON_COLUMN, "Total Flow (scfh)");
	lct_print_param(MON_FTO_ROW, MON_COLUMN, "F/O Ratio");

	lct_print_text(MON_MSG_ROW, 0, "Press \"Q\" to exit.");

	lct_setup_keypress();
	go_f = 1;
	
	// Start streaming gas data
	if(lc_stream_start(&dconf[MON_GASDEV], dconf[MON_GASDEV].nsample)){
		halt();
	}
	
	while(go_f){
		// Wait for data to arrive on the buffer
		while(lc_stream_isempty(&dconf[MON_GASDEV])){
			if(lc_stream_service(&dconf[MON_GASDEV])){
				halt();
			}
		}
		// Get the mean of the data waiting on the buffer
		lct_stream_mean(&dconf[MON_GASDEV], values, 2);
		fg = values[MON_FG_CHANNEL];
		o2 = values[MON_O2_CHANNEL];
		// Apply the channel calibrations
		lct_cal(&dconf[MON_GASDEV], MON_FG_CHANNEL, &fg);
		lct_cal(&dconf[MON_GASDEV], MON_O2_CHANNEL, &o2);
		
		lc_update_ef(&dconf[MON_RPMDEV]);
	
		if(dconf[MON_RPMDEV].efch[0].time){
			lct_print_flt(MON_RPM_ROW, MON_COLUMN, 0.5*1e6/dconf[MON_RPMDEV].efch[0].time);
			lct_print_flt(MON_RPM_ROW+1, MON_COLUMN, 0.5*60e6/dconf[MON_RPMDEV].efch[0].time);
		}else{
			lct_print_flt(MON_RPM_ROW, MON_COLUMN, 0);
			lct_print_flt(MON_RPM_ROW+1, MON_COLUMN, 0);
		}

		lct_print_flt(MON_O2_ROW, MON_COLUMN, o2);
		lct_print_flt(MON_FG_ROW, MON_COLUMN, fg);
		lct_print_flt(MON_FLOW_ROW, MON_COLUMN, fg+o2);
		lct_print_flt(MON_FTO_ROW, MON_COLUMN, fg / o2);

		// Check for exit condition
		if(lct_is_keypress())
			go_f = (getc(stdin) != 'Q');
			
	}
	lct_finish_keypress();
	
	lc_stream_stop(&dconf[MON_GASDEV]);
	lc_close(&dconf[MON_GASDEV]);
	lc_close(&dconf[MON_RPMDEV]);
	
	return 0;
}
