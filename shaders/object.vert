#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 cameraTransform;
uniform mat4 cameraProjection;

out vec4 trNormal;

void main(){
    gl_Position = cameraProjection * cameraTransform * vec4(position, 1);
    trNormal = inverse(transpose(cameraTransform)) * vec4(normal, 0);
}