#version 330 core

in vec2 uv;

uniform sampler2D char_bitmap;
uniform vec3 color;

out vec4 fragColor;

void main(){
    float texColor = texture(char_bitmap, uv).r;
    fragColor = vec4(color, texColor);
}