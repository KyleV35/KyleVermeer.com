/* Globals

canvas - the canvas context to draw to

*/

/* Constants */

var BRICK_WIDTH = 25;
var BRICK_SPACING_X = 3;
var BRICK_SPACING_Y = 2;
var BRICK_HEIGHT = 15;
var NUM_ROWS = 10;
var NUM_BRICKS_PER_ROW=20;
var BALL_RADIUS= 10;
var INITIAL_VX = 1;
var INITIAL_VY = 1;
var ONE_FRAME_TIME = 1000/30;
var PADDLE_OFFSET_FROM_BOTTOM = 50;
var PADDLE_WIDTH = 50;
var PADDLE_HEIGHT = 15;
var PADDLE_MOVE_AMOUNT = 5;
var TEXT_VERTICAL_SHIFT= -50;
var START_SPEED = 75;
var BRICK_COLORS = ["#000000","#DD0000","#DDDD00","#00DD00","#0000DD"];
var ROWS_PER_COLOR = 2;

var canvas_element= null;
var submit_button = null
var canvas = null;
var bricks = [];
var ball = null;
var paddle= null;
var paused = true;
var mainloop = null;
var game_over = false;
var speed = 0;
var score = 0;
var bricks_left = 0;

var input_form = null;
var high_score_name_input = null;

function create_game(canvasID,canvas_div, submit_button_selector,high_score_name_selector,input_form_selector) {
    submit_button = $(submit_button_selector);
    high_score_name_input = $(high_score_name_selector);
    console.log(submit_button);
    submit_button.click(function() {
        game_over_function();
    });
    canvas_element= document.getElementById(canvasID);
    var canvas_div = $("#"+canvas_div);
    input_form = $(input_form_selector);
    canvas= canvas_element.getContext("2d");
    adjust_canvas_width_to_game_size(canvas_div);
    set_up_game();
    create_key_bindings();
    create_mouse_bindings(canvas_div);
}

function set_up_game() {
    clear_canvas();
    draw_opening_text();
    game_over = false;
    paused=true;
    var width= canvas_element.width;
    var height= canvas_element.height;
    speed = START_SPEED;
    score = 0;
    hide_input();
    update_scoreboard();
    create_ball(width,height);
    create_paddle(width,height);
    create_bricks();
}

function hide_input() {
    if (input_form) {
        input_form.hide();
    }
}

function create_ball(canvas_width, canvas_height) {
    ball = new Ball(canvas_width/2,canvas_height/2,BALL_RADIUS,INITIAL_VX,INITIAL_VY);
    ball.draw();
}

function create_paddle(canvas_width,canvas_height) {
    paddle = new Paddle((canvas_width/2)-(PADDLE_WIDTH/2),canvas_height-PADDLE_OFFSET_FROM_BOTTOM,PADDLE_WIDTH,PADDLE_HEIGHT);
    paddle.draw();
}

function create_bricks() {
    bricks = [];
    make_n_rows(NUM_ROWS,1,1,BRICK_WIDTH,BRICK_SPACING_X, BRICK_SPACING_Y,BRICK_HEIGHT,NUM_BRICKS_PER_ROW);
    bricks_left= NUM_ROWS * NUM_BRICKS_PER_ROW;
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
    if (!game_over) {
        var cur_speed = speed/20;
        if (cur_speed <= 0) {
            speed= 20;
            cur_speed =1;
        }
        for (var i=0; i <cur_speed; i++) {
            clear_canvas();
            draw_bricks();
            paddle.draw();
            ball.move();
            ball.draw();
        }
        if (bricks_left == 0) {
            level_complete();
        }
    } else {
        clearInterval(mainloop);
        display_game_over();
        $(".high_score_input").show();
    }
}

function game_over_function() {
    var name = high_score_name_input.val();
    $.post("brickbreaker/highScore", {
        name: name,
        score: score
        }, function(data) {
        alert(data);
    });
    set_up_game();
            
}

function level_complete() {
    var width= canvas_element.width;
    var height= canvas_element.height;
    canvas.textAlign ="center";
    canvas.font = "bold 14px serif";
    canvas.fillText("Level Complete!",width/2, height/2 - TEXT_VERTICAL_SHIFT);
}

function display_game_over() {
    var width= canvas_element.width;
    var height= canvas_element.height;
    if (input_form) {
        input_form.show();
    }
    clear_canvas();
    canvas.textAlign ="center";
    canvas.font = "bold 14px serif";
    canvas.fillText("Game Over! Press Space to Play Again!",width/2, height/2 - TEXT_VERTICAL_SHIFT);
}

function draw_opening_text() {
    var width= canvas_element.width;
    var height= canvas_element.height;
    canvas.fillStyle= "#000000";
    canvas.textAlign = "center";
    canvas.font = "bold 14px serif";
    canvas.fillText("Welcome to Brick Breaker!  Press Space to Start!",width/2, height/2 - TEXT_VERTICAL_SHIFT);
}

function adjust_canvas_width_to_game_size(canvas_div) {
    // The 2 at the end adds some slight spacing from the edges
    canvas_element.width = NUM_BRICKS_PER_ROW*BRICK_WIDTH + (NUM_BRICKS_PER_ROW-1)*BRICK_SPACING_X + 2;
    canvas_div.css("width", canvas_element.width +"px");
}

function create_key_bindings() {
    $(document).keypress(function(event) {
        //console.log(event.which);
        if (event.which == 32) {
            if (!game_over) {
                if (paused) {
                    resume();
                } else {
                    pause();
                }
            } else {
                //Game is over
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

function resume() {
    mainloop= setInterval(play_game,ONE_FRAME_TIME);
    paused= false;
}

function pause() {
    var width= canvas_element.width;
    var height= canvas_element.height;
    clearInterval(mainloop);
    paused=true;
    canvas.textAlign = "center";
    canvas.font = "bold 14px serif";
    canvas.fillText("Game Paused! Press Space to Resume!",width/2, height/2 - TEXT_VERTICAL_SHIFT);
}

function create_mouse_bindings(canvas_div) {
    $(document).mousemove(function(event) {
        var mouse_position = (event.pageX - canvas_div.offset().left);
        paddle.set_position(mouse_position);
    });
}

function clear_canvas() {
    canvas.clearRect(0, 0, canvas_element.width, canvas_element.height);
}

function make_row(start_x, spacing, start_y, brick_height, num_bricks, row_group,color) {
    var x=start_x;
    var total_row_groups = NUM_ROWS/ROWS_PER_COLOR;
    for (var i=0; i <num_bricks; i++) {
        bricks.push(new Brick(x,start_y,BRICK_WIDTH,brick_height,(total_row_groups-row_group)*10,color));
        x= x+BRICK_WIDTH+spacing;
    }
}

function make_n_rows(num_rows, start_x, start_y, brick_width, x_spacing, y_spacing, brick_height, num_bricks_per_row) {
    var y = start_y;
    for (var i=0; i < num_rows; i++) {
        var color = "#000000";
        var row_group = Math.floor(i/ROWS_PER_COLOR);
        if (row_group == 0) {
            color = "#DDDD00";
        } else if (row_group == 1) {
            color = "#00DDAA";
        } else if (row_group == 2) {
            color = "#00DDDD";
        } else if (row_group == 3) {
            color ="#0000DD";
        } else if (row_group == 4) {
            color ="#DD00DD";
        }
        //var color = BRICK_COLORS[row_group];
        make_row(start_x,x_spacing,y,brick_height,num_bricks_per_row,row_group,color);
        y= y +brick_height + y_spacing;
    }
}

function Brick(left_x,top_y,width,height, score, color) {
    this.x= left_x;
    this.y= top_y;
    this.width= width;
    this.height= height;
    this.color= color
    this.score= score;
    
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
    this.momentum = 0;
    
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
    
    this.set_position = function(new_x) {
        this.momentum = new_x  - this.width/2 - this.x;
        this.x = new_x - this.width/2;
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
        this.check_brick_collision(new_x,new_y, false);
        this.check_paddle_collision(new_x,new_y);
        
    }
    
    this.check_wall_collision = function(new_x,new_y) {
        if ((new_x + this.radius) >= canvas_element.width) {
            if (this.vx > 0) {
                this.vx = -this.vx;
            }
            return true;
        } else if ((new_x-this.radius) <= 0.0) {
            if (this.vx < 0) {
                this.vx = -this.vx;
                return true;
            }
        }
        if ((new_y + this.radius) >= canvas_element.height) {
            game_over = true;
            return true;
        } else if ((new_y-this.radius) <=0.0) {
            this.vy = -this.vy;
            return true;
        }
        return false;
    }
    
    this.check_brick_collision= function(new_x,new_y, has_been_collision) {
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
                    if ((top_y_ball > top_y_brick && top_y_ball < bottom_y_brick) ||
                    (bottom_y_ball > top_y_brick && bottom_y_ball < bottom_y_brick)) {
                        score = score + bricks[i].score;
                        bricks_left= bricks_left-1;
                        update_scoreboard();
                        bricks[i] = null;
                        if (this.vy < 0) {
                            this.vy= -this.vy;
                        } else if (new_x > left_x_brick) { /* This is an attempt to only bounce you up at correct times */
                            this.vy = -this.vy;
                        } else {
                            this.vx = -this.vx;
                        }
                        temp_vy = this.vy;
                        temp_vx = this.vx;
                        check_y = this.y + this.vy;
                        check_x = this.x +this.vx;
                        if (!has_been_collision && this.check_brick_collision(check_x,check_y,true)) {
                            this.vy= temp_vy;
                            this.vx = temp_vx;
                        }
                        ball.draw();
                        return true;
                    }
                }
                // Ball Moving left
                else if (left_x_ball > left_x_brick && left_x_ball < right_x_brick) {
                    if ((top_y_ball > top_y_brick && top_y_ball < bottom_y_brick) ||
                    (bottom_y_ball > top_y_brick && bottom_y_ball < bottom_y_brick)) {
                        score = score + bricks[i].score;
                        bricks_left = bricks_left-1;
                        update_scoreboard();
                        bricks[i] = null;
                        if (this.vy < 0) {
                            this.vy= -this.vy;
                        } else if (new_x < right_x_brick) { /* This is an attempt to only bounce you up at correct times */
                            this.vy = -this.vy;
                        } else {
                            this.vx = -this.vx;
                        }
                        temp_vy = this.vy;
                        temp_vx = this.vx;
                        check_y = this.y + this.vy;
                        check_x = this.x +this.vx;
                        if (!has_been_collision && this.check_brick_collision(check_x,check_y,true)) {
                            this.vy= temp_vy;
                            this.vx = temp_vx;
                        }
                        ball.draw();
                        return true;
                    }
                }
            }
        }
        return false;
    }
    
    this.check_paddle_collision = function(x,y) {
        var radius = this.radius;
        var right_x_ball = x + radius;
        var left_x_ball = x - radius;
        var top_y_ball = y - radius;
        var bottom_y_ball = y + radius;
        var right_x_paddle = paddle.x+ paddle.width;
        var left_x_paddle = paddle.x;
        var top_y_paddle = paddle.y;
        var bottom_y_paddle = paddle.y+paddle.height;
        if (right_x_ball < right_x_paddle && right_x_ball > left_x_paddle) {
            if (bottom_y_ball > top_y_paddle && bottom_y_ball < bottom_y_paddle) {
                if (this.vy > 0) {
                    this.vy= -this.vy;
                }
                if (this.vx >0 && paddle.momentum > 0) {
                    speed = speed+paddle.momentum;
                } else if (this.vx < 0 && paddle.momentum < 0) {
                    speed = speed-paddle.momentum;
                } else if (paddle.momentum ==0) {
                    
                } else {
                    speed = speed-paddle.momentum;
                }
                console.log("VX: " + this.vx);
                console.log("Momentum: " + paddle.momentum);
                console.log("Speed: " + speed);
                return true;
            }
        }
        else if (left_x_ball > left_x_paddle && left_x_ball < right_x_paddle) {
            if (bottom_y_ball > top_y_paddle && bottom_y_ball < bottom_y_paddle) {
                if (this.vy > 0) {
                    this.vy= -this.vy;
                }
                if (this.vx >0 && paddle.momentum > 0) {
                    speed = speed+paddle.momentum;
                } else if (this.vx < 0 && paddle.momentum < 0) {
                    speed = speed-paddle.momentum; // Momentum is negative, will increase speed
                } else if (paddle.momentum ==0) {
                    
                } else {
                    if (paddle.momentum > 0) {
                        speed = speed-paddle.momentum;
                    } else {
                        speed = speed+paddle.momentum;
                    }
                }
                console.log("VX: " + this.vx);
                console.log("Momentum: " + paddle.momentum);
                console.log("Speed: " + speed);
                return true;
            }
        }
    }
}

function update_scoreboard() {
    $("#score_span").text(score);
}