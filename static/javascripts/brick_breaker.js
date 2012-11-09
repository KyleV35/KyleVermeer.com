/* Globals

canvas - the canvas context to draw to

*/

function create_game(canvasID) {
    var canvas_element= document.getElementById(canvasID);
    canvas= canvas_element.getContext("2d");
    canvas.fillStyle="#FF0000";
    draw_n_rows(5,0,20,2,2,10,20);
    canvas.fillStyle="#000000";
    draw_ball(220,100,25);    
}

function draw_row(start_x, brick_width, spacing, start_y, brick_height, num_bricks) {
    var x=start_x;
    for (var i=0; i <num_bricks; i++) {
        canvas.fillRect(x,start_y,brick_width,brick_height);
        x= x+brick_width+spacing;
    }
}

function draw_n_rows(num_rows, start_x, brick_width, x_spacing, y_spacing, brick_height, num_bricks_per_row) {
    var y = 0;
    for (var i=0; i < num_rows; i++) {
        draw_row(start_x,brick_width,x_spacing,y,brick_height,num_bricks_per_row);
        y= y +brick_height + y_spacing;
    }
}

function draw_ball(center_x,center_y,radius) {
    canvas.beginPath();
    canvas.arc(center_x,center_y,radius,0,2*Math.PI);
    canvas.fill();
}