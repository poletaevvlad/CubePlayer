#version 330 core

#define LIGHTS_COUNT 2

struct DirectionalLight{
    vec3 color;
    vec3 direction;
};


in vec3 trNormal;
in vec3 worldPos;
out vec4 fragColor;
uniform DirectionalLight lights[LIGHTS_COUNT];


vec3 computeDuffuse(DirectionalLight light, vec3 normal){
    float diffuse = max(dot(normal, light.direction), 0.0);
    return diffuse * light.color;
}


vec3 computeSpecular(DirectionalLight light, vec3 normal, vec3 viewDirection){
    vec3 reflectDirection = reflect(-light.direction, normal);
    float specular = pow(max(dot(viewDirection, reflectDirection), 0.0), 10);
    return specular * light.color;
}


void main(){
    vec3 normal = normalize(trNormal.xyz);
    vec3 viewDir = normalize(-worldPos);

    vec3 ambient = vec3(1.0, 1.0, 1.0) * 0.1;
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);

    for (int i = 0; i < LIGHTS_COUNT; i++){
        diffuse += computeDuffuse(lights[i], normal);
        specular += computeSpecular(lights[i], normal, viewDir);
    }

    vec3 materialColor = vec3(worldPos / 10 + 0.5);
    fragColor = vec4(materialColor * (ambient + diffuse + specular), 1);
}