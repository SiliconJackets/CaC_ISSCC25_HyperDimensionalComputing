module mem_clean_up #(
    parameter VECTOR_LEN,
    parameter VECTOR_LEN_LOG_2 = $clog2(VECTOR_LEN), // Number of bits required to represent a bipolar vector in 2s complement
    parameter NUM_CODEBOOK_BITS = 4,

    // Matrix representing the codebook for the feature this module is targeting, X, times its transpose, XT.
    parameter logic signed [VECTOR_LEN-1 : 0][VECTOR_LEN-1 : 0][NUM_CODEBOOK_BITS-1 : 0] XXT
)(
    input  logic [VECTOR_LEN-1 : 0] x_hat_in, // Vector representing the current prediction for the feature this module is targeting
    output logic [VECTOR_LEN-1 : 0] x_hat_out // The prediction vector projected onto the span of the Codebook
);
    // The result of feature_binding x_hat_in with each column of XXT
    logic signed [VECTOR_LEN-1 : 0][VECTOR_LEN-1 : 0][NUM_CODEBOOK_BITS-1 : 0] partial_feature_binded_x_hat;


    // // feature_binded_x_hat represented in 2s complement instead of bipolar vectors
    // logic signed [VECTOR_LEN-1 : 0][VECTOR_LEN_LOG_2-1 : 0] feature_binded_2s_x_hat; 



    // Project x_hat onto the span of X using matrix-vector multiplication
    generate
        for (genvar i = 0; i < VECTOR_LEN; i = i + 1) begin


            // Start by multiplying every row of XXT by x_hat_in
            for (genvar j = 0; j < VECTOR_LEN; j = j + 1) begin
                // If x_hat is -1, flip the sign of XXT and store
                always_comb begin
                    if (x_hat_in[j]) begin
                        partial_feature_binded_x_hat[i][j][NUM_CODEBOOK_BITS-1 : 0] = ~XXT[i][j][NUM_CODEBOOK_BITS-1 : 0] + $signed(1'b1);
                    end else begin
                        // if x_hat is 1, keep XXT the same
                        partial_feature_binded_x_hat[i][j][NUM_CODEBOOK_BITS-1 : 0] = XXT[i][j][NUM_CODEBOOK_BITS-1 : 0];
                    end
                end
            end

            // Now sum each row together and threshold to bipolar value to get new x_hat prediction. 
            bipolar_sum_tree bst_0 (
                .inner_partial_products(partial_feature_binded_x_hat[i]),
                .bipolar_value(x_hat_out[i])
            );
        end
    endgenerate
endmodule