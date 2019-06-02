#version 330 core

layout(location = 0) in vec2 position;

out float x;
out float y;


void main(){
    gl_Position = vec4(position, 0, 1);
    y = (1 - position.y) / 2;
    x = position.x;
}