module factor_feature #(
    parameter VECTOR_LEN = 32,
    parameter NUM_CODEBOOK_BITS = 4, // Minimum number of bits required to represent the number of codebook vectors in the codebook

    // Matrix representing the codebook for the feature this module is targeting, X, times its transpose, XT.
    parameter logic signed [VECTOR_LEN-1 : 0][VECTOR_LEN-1 : 0][NUM_CODEBOOK_BITS-1 : 0] XXT
)(
    input logic i_clk,
    input logic i_rstn,


    input  logic[VECTOR_LEN-1 : 0] s_in, // Vector representing our HyperDimensional Scene
    input  logic[VECTOR_LEN-1 : 0] o_hat_in, // Vector representing the feature_binding of all other features predictions(x_hat, y_hat, etc) in the current scene

    output logic converged_out, // 1 bit vector denoting if this feature has converged
    output logic[VECTOR_LEN-1 : 0] x_hat_out // Vector representing the current prediction for the feature this module is targeting
);
    // Current prediction for the current feature
    logic[VECTOR_LEN-1 : 0] x_hat;
    logic converged_next;

    // Register holding prediction to be outputted next cycle
    logic[VECTOR_LEN-1 : 0] x_hat_next;

    feature_bind #(VECTOR_LEN) b_0 (
        .a_in(s_in),
        .b_in(o_hat_in),
        .out(x_hat)
    );

    mem_clean_up #(
        .VECTOR_LEN(VECTOR_LEN), 
        .XXT(XXT)
    ) clean (
        .x_hat_in(x_hat),
        .x_hat_out(x_hat_next)
    );


    // Test convergence
    always_comb begin
        if (x_hat === x_hat_next) begin
            converged_next = 1'b1;
        end else begin 
            converged_next = 1'b0;
        end
    end


    always_ff @(posedge i_clk, negedge i_rstn) begin
        if(i_rstn === 1'b0) begin
            x_hat_out <= '0;
            converged_out <= 1'b0;
        end
        else begin
            x_hat_out     <= x_hat_next;
            converged_out <= converged_next;
        end
    end
    


endmodule