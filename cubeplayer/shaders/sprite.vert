#version 330 core

layout(location = 0) in vec2 position;

out vec2 uv;

uniform vec2 screen_size;
uniform vec2 location;
uniform vec2 size;

void main(){
    vec2 loc = vec2(location.x, screen_size.y - location.y);
    vec2 pos01 = (position + 1) * 0.5;
    vec2 left_top = (loc - vec2(0, size.y)) / screen_size;
    vec2 right_bottom = (loc + size - vec2(0, size.y)) / screen_size;
    gl_Position = vec4((left_top + pos01 * (right_bottom - left_top)) * 2 - 1, 0, 1);

    uv = vec2((position.x + 1) * 0.5, (1 - position.y) * 0.5);
}