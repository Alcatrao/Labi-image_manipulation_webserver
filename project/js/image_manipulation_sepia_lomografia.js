function manipulateImage_sepia_lomografia(file) {                       
    if(file != null) {
        sendFile_sepia_lomografia(file);
    }
    else alert("Image missing!");
}

function sendFile_sepia_lomografia(file) {
	
    var sepia_lomografia = document.getElementById("bw_sepia_lomografia").checked;


        var data = new FormData();
        data.append("file", file)
        data.append("sepia_lomografia", sepia_lomografia)
        
                                
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/sepsis_lomography");  


        xhr.onreadystatechange = () => {                                            
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
                show_manipulated_image_sepia_lomografia(JSON.parse( xhr.response ));       
                }
            };

            xhr.send(data);

}



function show_manipulated_image_sepia_lomografia(response) {     //mostra a imagem  manipulada

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "sepia_lomografia_falhou") {
        let image = document.createElement("img");
        image.src = "../"+response["result"];         
        image.width = "550";
        image.height = "450";
        document.getElementById("manipulated_image").appendChild(image);
    }
    else {
        alert("Sepsis/Lomography could not be applied to the chosen image.");
    }
    

    
}


function im_inputs_sepia_lomografia() {
 
    var divs = document.createElement("div");

    //criar input True or False para o parâmetro "sepia_lomografia"
    var select_sepia_lomografia = document.createElement("input");
    select_sepia_lomografia.type = "checkbox";
    select_sepia_lomografia.value = "on";
    select_sepia_lomografia.id = "bw_sepia_lomografia";

    var label_select = document.createElement("label");
    label_select.innerHTML = "Uncheck for Sepsis, check for Lomography";
    label_select.setAttribute("for", select_sepia_lomografia.id);

    divs.appendChild(label_select);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(select_sepia_lomografia);


    //dar append de ambos à div abaixo das duas divs principais (da escolher foto, e da imagem manipulada)
    document.getElementById("other_image").appendChild(divs);
    
}


export {manipulateImage_sepia_lomografia, sendFile_sepia_lomografia, show_manipulated_image_sepia_lomografia, im_inputs_sepia_lomografia};