#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 cameraTransform;

void main(){
    gl_Position = cameraTransform * vec4(position, 1);
}