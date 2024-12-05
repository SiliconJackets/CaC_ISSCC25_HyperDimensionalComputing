// `include "res_net_pkg.svh"
import RES_NET_PKG::*;

module res_net_top (
    input logic i_clk,
    input logic i_rstn,
    input logic i_init,
    
    // Hyperdimensional representation of a scene
    input  logic [VECTOR_LEN-1 : 0] scene_in,

    input logic [VECTOR_LEN-1 : 0] color_init,
    input logic [VECTOR_LEN-1 : 0] shape_init,
    input logic [VECTOR_LEN-1 : 0] position_init,


    // Predictions for each of the features, these take the form of the index in the codebook of the predicted feature
    output logic color_converged,
    output logic shape_converged,
    output logic position_converged,


    output logic [VECTOR_LEN-1 : 0] color_prediction,
    output logic [VECTOR_LEN-1 : 0] shape_prediction,
    output logic [VECTOR_LEN-1 : 0] position_prediction

);


    // Feedback loop for color prediction
    //logic color_converged;
    //logic [VECTOR_LEN-1 : 0] color_prediction;
    logic [VECTOR_LEN-1 : 0] color_o_hat;

    // Feedback loop for color prediction
    //logic position_converged;
    //logic [VECTOR_LEN-1 : 0] position_prediction;
    logic [VECTOR_LEN-1 : 0] position_o_hat;

    // Feedback loop for color prediction
    //logic shape_converged;
    //logic [VECTOR_LEN-1 : 0] shape_prediction;
    logic [VECTOR_LEN-1 : 0] shape_o_hat;


    feature_bind #(
        .VECTOR_LEN(VECTOR_LEN)
    ) feature_bind_color_components (
        .a_in(i_init? shape_init : shape_prediction),
        .b_in(i_init? position_init : position_prediction),
        .out(color_o_hat)
    );

    factor_feature #(
        .VECTOR_LEN(VECTOR_LEN),
        .NUM_CODEBOOK_BITS(NUM_CODEBOOK_BITS),
        .XXT(CCT)
    ) factor_color (
        .i_clk(i_clk),
        .i_rstn(i_rstn),

        .s_in(scene_in),
        .o_hat_in(color_o_hat),

        .converged_out(color_converged),
        .x_hat_out(color_prediction)
    );




    feature_bind #(
        .VECTOR_LEN(VECTOR_LEN)
    ) feature_bind_shape_components (
        .a_in(i_init? color_init : color_prediction),
        .b_in(i_init? position_init : position_prediction),
        .out(shape_o_hat)
    );

    factor_feature #(
        .VECTOR_LEN(VECTOR_LEN),
        .NUM_CODEBOOK_BITS(NUM_CODEBOOK_BITS),
        .XXT(SST)
    ) factor_shape (
        .i_clk(i_clk),
        .i_rstn(i_rstn),

        .s_in(scene_in),
        .o_hat_in(shape_o_hat),

        .converged_out(shape_converged),
        .x_hat_out(shape_prediction)
    );





    feature_bind #(
        .VECTOR_LEN(VECTOR_LEN)
    ) feature_bind_position_components (
        .a_in(i_init? color_init : color_prediction),
        .b_in(i_init? shape_init : shape_prediction),
        .out(position_o_hat)
    );

    factor_feature #(
        .VECTOR_LEN(VECTOR_LEN),
        .NUM_CODEBOOK_BITS(NUM_CODEBOOK_BITS),
        .XXT(PPT)
    ) factor_position (
        .i_clk(i_clk),
        .i_rstn(i_rstn),

        .s_in(scene_in),
        .o_hat_in(position_o_hat),

        .converged_out(position_converged),
        .x_hat_out(position_prediction)
    );
endmodule