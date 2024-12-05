module feature_bind #(
    parameter VECTOR_LEN
) (
    input  logic[VECTOR_LEN-1 : 0] a_in,
    input  logic[VECTOR_LEN-1 : 0] b_in,
    output logic[VECTOR_LEN-1 : 0] out
);

    // Represent element wise multiplication as the xor of corresponding elements in a & b. 
    // This works because we have encoded 1 as 1'b0 & -1 as 1'b1.
    assign out = a_in ^ b_in;
    
endmodule