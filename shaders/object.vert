#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 cameraTransform;
uniform mat4 cameraProjection;
uniform mat4 objectTransform;

out vec4 trNormal;

void main(){
    mat4 transform = cameraTransform * objectTransform;
    gl_Position = cameraProjection * transform * vec4(position, 1);
    trNormal = inverse(transpose(transform)) * vec4(normal, 0);
}