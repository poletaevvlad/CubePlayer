#version 330 core

in vec4 trNormal;
out vec4 fragColor;

void main(){
    vec4 normal = trNormal;
    normal.w = 1;

    fragColor = normal;
}