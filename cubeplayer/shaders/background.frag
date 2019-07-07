#version 330 core

out vec4 fragColor;

in float x;
in float y;

uniform vec3 colorFrom;
uniform vec3 colorTo;

void main(){
    float ratio = pow(y, 2 + 2 * pow(x, 2));
    vec3 color = colorFrom * ratio + colorTo * (1 - ratio);

    fragColor = vec4(color, 1);
}