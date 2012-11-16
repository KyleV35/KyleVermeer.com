/* Globals

canvas - the canvas context to draw to

*/

/* Constants */

var BRICK_WIDTH = 20.0;
var BRICK_SPACING_X = 3.0;
var BRICK_SPACING_Y = 2.0;
var BRICK_HEIGHT = 10.0;
var NUM_ROWS = 10.0;
var NUM_BRICKS_PER_ROW=20.0;
var BALL_RADIUS= 10.0;
var INITIAL_VX = 2.5;
var INITIAL_VY = 2.5;
var ONE_FRAME_TIME = 1000/60;
var PADDLE_OFFSET_FROM_BOTTOM = 50;
var PADDLE_WIDTH = 50;
var PADDLE_HEIGHT = 15;
var PADDLE_MOVE_AMOUNT = 5;

var canvas_element;
var canvas = null;
var bricks = [];
var ball = null;
var paddle= null;
var paused = true;
var mainloop = null;

function create_game(canvasID,canvas_div) {
    canvas_element= document.getElementById(canvasID);
    var canvas_div = document.getElementById(canvas_div);
    canvas= canvas_element.getContext("2d");
    set_up_game(canvas_div);
    create_key_bindings();
}

function set_up_game(canvas_div) {
    adjust_canvas_width_to_game_size(canvas_div);
    var width= canvas_element.width;
    var height= canvas_element.height;
    ball = new Ball(width/2.0,height/2.0,BALL_RADIUS,INITIAL_VX,INITIAL_VY);
    ball.draw();
    paddle = new Paddle((width/2.0)-(PADDLE_WIDTH/2.0),height-PADDLE_OFFSET_FROM_BOTTOM,PADDLE_WIDTH,PADDLE_HEIGHT);
    paddle.draw();
    make_n_rows(NUM_ROWS,1.0,1.0,BRICK_WIDTH,BRICK_SPACING_X, BRICK_SPACING_Y,BRICK_HEIGHT,NUM_BRICKS_PER_ROW);
    draw_bricks();
}

function draw_bricks() {
    var num_bricks = bricks.length;
    for (var i=0; i < num_bricks; i++) {
        if (bricks[i]!=null) {
            bricks[i].draw();
        }
    }
}

function play_game() {
    clear_canvas();
    draw_bricks();
    paddle.draw();
    ball.move();
    ball.draw();
}

function adjust_canvas_width_to_game_size(canvas_div) {
    console.log(canvas_div);
    // The 2 at the end adds some slight spacing from the edges
    canvas_element.width = NUM_BRICKS_PER_ROW*BRICK_WIDTH + (NUM_BRICKS_PER_ROW-1)*BRICK_SPACING_X + 2;
    canvas_div.style.width= canvas_element.width +"px";
}

function create_key_bindings() {
    $(document).keypress(function(event) {
        //console.log(event.which);
        if (event.which == 32) {
            if (paused) {
                mainloop= setInterval(play_game,ONE_FRAME_TIME);
                paused= false;
            } else {
                clearInterval(mainloop);
                paused=true;
            }
        }
        else if (event.which == 97 || event.which == 37) {
            paddle.move(-PADDLE_MOVE_AMOUNT);
        }
        else if (event.which == 100 || event.which == 39) {
            paddle.move(PADDLE_MOVE_AMOUNT);
        }
    });
    
}

function clear_canvas() {
    canvas.clearRect(0, 0, canvas_element.width, canvas_element.height);
}

function make_row(start_x, spacing, start_y, brick_height, num_bricks) {
    var x=start_x;
    for (var i=0; i <num_bricks; i++) {
        bricks.push(new Brick(x,start_y,BRICK_WIDTH,brick_height,"#FF0000"));
        x= x+BRICK_WIDTH+spacing;
    }
}

function make_n_rows(num_rows, start_x, start_y, brick_width, x_spacing, y_spacing, brick_height, num_bricks_per_row) {
    var y = start_y;
    for (var i=0; i < num_rows; i++) {
        make_row(start_x,x_spacing,y,brick_height,num_bricks_per_row);
        y= y +brick_height + y_spacing;
    }
}

function Brick(left_x,top_y,width,height, color) {
    this.x= left_x;
    this.y= top_y;
    this.width= width;
    this.height= height;
    this.color= color
    
    this.draw = function() {
        canvas.fillStyle = this.color;
        canvas.fillRect(this.x,this.y,this.width,this.height);
    }
}

function Paddle(left_x,top_y,width,height,color) {
    this.x= left_x;
    this.y= top_y;
    this.width= width;
    this.height= height;
    if (color == null) {
        this.color= "#000000";
    } else {
        this.color= color;
    }
    
    this.draw = function() {
        canvas.fillStyle = this.color;
        canvas.fillRect(this.x,this.y,this.width,this.height);
    }
    
    this.move = function (shift_x) {
        this.x = this.x+shift_x;
    }
}

function Ball(center_x,center_y,radius, velocity_x, velocity_y,color) {
    this.x= center_x;
    this.y= center_y;
    this.radius = radius;
    this.vx= velocity_x;
    this.vy= velocity_y;
    if (color == null) {
        this.color= "#000000";
    } else {
        this.color= color;
    }
    
    this.draw = function() {
        canvas.fillStyle = this.color;
        canvas.beginPath();
        canvas.arc(this.x,this.y,this.radius,0,2*Math.PI);
        canvas.fill();
    }
    
    this.move = function() {
        var new_x = this.x+this.vx
        var new_y = this.y+this.vy
        this.x = new_x;
        this.y= new_y;
        
        this.check_wall_collision(new_x,new_y);
        this.check_brick_collision(new_x,new_y);
        
    }
    
    this.check_wall_collision = function(new_x,new_y) {
        if ((new_x + this.radius) >= canvas_element.width || (new_x-this.radius) <= 0.0) {
            this.vx = -this.vx;
        }
        if ((new_y + this.radius) >= canvas_element.height || (new_y-this.radius) <=0.0) {
            this.vy = -this.vy;
        }
    }
    
    this.check_brick_collision= function(new_x,new_y) {
        var num_bricks = bricks.length;
        for (var i=0; i < num_bricks; i++) {
            brick= bricks[i];
            if (brick!=null) {
                var radius= this.radius;
                var right_x_ball = new_x + radius;
                var left_x_ball = new_x - radius;
                var top_y_ball = new_y - radius;
                var bottom_y_ball = new_y + radius;
                var right_x_brick = brick.x+brick.width;
                var left_x_brick = brick.x;
                var top_y_brick = brick.y;
                var bottom_y_brick = brick.y+brick.height;
                // Ball moving right
                if (right_x_ball < right_x_brick && right_x_ball > left_x_brick) {
                    if (top_y_ball > top_y_brick && top_y_ball < bottom_y_brick) {
                        bricks[i] = null;
                        if (this.vy < 0) {
                            this.vy= -this.vy;
                        } else if (new_x > left_x_brick) { /* This is an attempt to only bounce you up at correct times */
                            this.vy = -this.vy;
                        } else {
                            this.vx = -this.vx;
                        }
                        break;
                    }
                }
                else if (left_x_ball > left_x_brick && left_x_ball < right_x_brick) {
                    if (top_y_ball > top_y_brick && top_y_ball < bottom_y_brick) {
                        bricks[i] = null;
                        if (this.vy < 0) {
                            this.vy= -this.vy;
                        } else if (new_x < right_x_brick) { /* This is an attempt to only bounce you up at correct times */
                            this.vy = -this.vy;
                        } else {
                            this.vx = -this.vx;
                        }
                        break;
                    }
                }
            }
        }
    }
}