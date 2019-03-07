#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 uv;

uniform mat4 cameraTransform;
uniform mat4 cameraProjection;
uniform mat4 objectTransform;
uniform mat4 tempTransform;

out vec3 trNormal;
out vec3 worldPos;
out vec2 texCoord;

void main(){
    mat4 transform = cameraTransform * tempTransform * objectTransform;

    vec4 camaraSpacePosition = transform * vec4(position, 1);
    gl_Position = cameraProjection * camaraSpacePosition;
    trNormal = (inverse(transpose(transform)) * vec4(normal, 0)).xyz;
    worldPos = camaraSpacePosition.xyz;
    texCoord = uv;
}