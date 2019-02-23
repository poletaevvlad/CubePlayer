#version 330 core

in vec3 trNormal;
in vec3 worldPos;

out vec4 fragColor;


vec3 computeDirectionalLight(vec3 viewDirection, vec3 lightDirection, vec3 normal){
    vec3 ambientLight = vec3(1, 1, 1) * 0.1;

    float diffuse = max(dot(normal, lightDirection), 0.0);
    vec3 diffuseLight = diffuse * vec3(1, 1, 1);

    vec3 reflectDirection = reflect(-lightDirection, normal);
    float specular = pow(max(dot(viewDirection, reflectDirection), 0.0), 10);

    vec3 specularLight = specular * vec3(1, 1, 1);

    return diffuseLight + specularLight;
}


void main(){
    vec3 normal = normalize(trNormal.xyz);
    vec3 viewDir = normalize(/* 0 */ - worldPos);

    vec3 lightDir = normalize(vec3(1, 1, 1));
    vec3 ambientLight = vec3(1,1,1) * 0.1;

    fragColor = vec4(ambientLight + computeDirectionalLight(viewDir, lightDir, normal), 1);
}