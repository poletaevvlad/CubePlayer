#version 330 core

out vec4 fragColor;

in float gradientRatio;
uniform vec3 colorFrom;
uniform vec3 colorTo;

void main(){
    vec3 color = colorFrom * gradientRatio + colorTo * (1 - gradientRatio);

    fragColor = vec4(color, 1);
}