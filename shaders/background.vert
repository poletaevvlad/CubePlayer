#version 330 core

layout(location = 0) in vec2 position;

out float gradientRatio;

void main(){
    gl_Position = vec4(position, 0, 1);
    gradientRatio = (1 - position.y) / 2;
}