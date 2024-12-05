
//Paramterizable tree so we can test different bit widths, when we settle on one(probably 16bits or so), I'll hardcode a good one
module bipolar_sum_tree #(
    parameter VECTOR_LEN = 32,
    parameter VECTOR_LEN_LOG_2 = $clog2(VECTOR_LEN),
    parameter NUM_CODEBOOK_BITS = 4
)(
    input  logic signed [VECTOR_LEN-1 : 0][3 : 0] inner_partial_products, // layer_0 -  32 4-bit numbers
    output logic signed bipolar_value
    // output logic signed [8 : 0] bipolar_value

);

    //logic signed [VECTOR_LEN-1 : 0][3 : 0] inner_partial_productssigned;
    //assign inner_partial_productssigned = inner_partial_products;
    // Partial products of our adder tree, note that the length of the final vector is: NUM_CODEBOOK_BITS + log2(VECTOR_LEN)
    logic signed [15 : 0][4 : 0] layer_1; // 16 5-bit numbers
    logic signed [7  : 0][5 : 0] layer_2; // 8 6-bit numbers
    logic signed [3  : 0][6 : 0] layer_3; // 4 7-bit numbers
    logic signed [1  : 0][7 : 0] layer_4; // 2 8-bit numbers
    logic signed         [8 : 0] layer_5; // 1 9-bit number

    generate
        for (genvar i = 0; i < 32; i = i + 2) begin
            always_comb begin
                layer_1[i>>1] = $signed(inner_partial_products[i] + inner_partial_products[i+1]);
            end
        end

        for (genvar j = 0; j < 16; j = j + 2) begin
            always_comb begin
                layer_2[j>>1] = $signed(layer_1[j] + layer_1[j+1]);
            end
        end

        for (genvar k = 0; k < 8; k = k + 2) begin
            always_comb begin
                layer_3[k>>1] = $signed(layer_2[k] + layer_2[k+1]);
            end
        end

        for (genvar l = 0; l < 4; l = l + 2) begin
            always_comb begin
                layer_4[l>>1] = $signed(layer_3[l] + layer_3[l+1]);
            end
        end

        // Threshold result to bipolar vector by returning the sign of the end vector
        always_comb begin
            layer_5       = $signed(layer_4[0] + layer_4[1]);
            bipolar_value = layer_5[8];
        end
    endgenerate
endmodule