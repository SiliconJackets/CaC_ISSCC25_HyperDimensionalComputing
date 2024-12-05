#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <verilated.h>
#include <verilated_vcd_c.h>
#include "Vres_net_pkg.h"

VerilatedVcdC*      trace = NULL;       // Waveform Generation
static Vres_net_pkg*        top;                // DUT
vluint64_t          sim_time = 0;       // Simultation time
const int           TESTCASE_SIZE = 3;  // Test cases per line

// Function to evaluate the DUT and dump waveforms
void eval_and_dump_wave() {

	top->eval();                // Evaluate the DUT
	trace->dump(sim_time++);    // Dump waveforms to VCD file and increment simulation time
}

// Function to execute a single clock cycle
void single_cycle() {

    top->i_clk = 0;               // Set clock low
    eval_and_dump_wave();       // Evaluate and dump waveforms
    top->i_clk = 1;               // Set clock high
    eval_and_dump_wave();       // Evaluate and dump waveforms
}

// Function to reset the DUT
void reset(int n) {

    top->i_rstn = 0;              // Assert reset
    while(n-->0)                // Loop for specified number of cycles
        single_cycle();
    top->i_rstn = 1;              // Deassert reset
}

// Function to initialize simulation
void sim_init(uint32_t scene) {

	trace       = new VerilatedVcdC; 
	top         = new Vres_net_pkg;
	top->trace(trace,0);        // Enable tracing and set start time
	trace->open("dump.vcd");    // Open VCD file for writing waveform

    top->i_init = 0;             // Initialize readA signal
    top->scene_in = scene;            // Initialize readB signal
    top->color_init = 2198453636;
    top->shape_init = 3215788617;
    top->position_init = 338248138;
    reset(2);                   // Reset the DUT for 2 cycles
    top->i_init = 1;
    single_cycle();
    top->i_init = 0;
}

// Function to finalize simulation and clean up
int sim_exit() {

	eval_and_dump_wave();
	top->final();               // Finalize DUT
	trace->close();             // Close VCD file
	delete top;                 // Delete DUT instance

    return EXIT_SUCCESS;
}

// Function to read in test case to a vector
void readNumbers(const std::string& filename, std::vector<int>& numbers) {
    
    // Open test case file
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }

    // Read test case file line by line, extract tokens separated by ','
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string token;
        while (std::getline(iss, token, ',')) {
            numbers.push_back(std::stoi(token));
        }
    }

    // Close test case file
    file.close();
}

// Test main
int main(int argc, char** argv) {

    uint32_t scene;
    scene = 969473173;

    if (argc > 1) {
      char* endptr;
      unsigned long int value = std::strtoul(argv[1], &endptr, 10);
      scene = static_cast<uint32_t>(value);
    }
    // Initialize test
    Verilated::commandArgs(argc, argv);
    Verilated::traceEverOn(true);
    sim_init();

    // Read in test cases
    std::vector<int> test_cases;
    //readNumbers("/content/convInput.txt", test_cases);
    int cycle = 100; //max iterations


    // Iterate
    for (int i = 0; i < cycle; i++) {
        if (top->color_converged && top->shape_converged && top->position_converged) {
          std::cout << "converged " << i+1 << " cycles" << std::endl;
          break;
        }
        single_cycle();
    }

    //dumpfile.close();

    return sim_exit();
}