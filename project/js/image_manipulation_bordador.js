function manipulateImage_bordador(file) {                       
    if(file != null) {
        sendFile_bordador(file);
    }
    else alert("Image missing!");
}

function sendFile_bordador(file) {
	
    var diff = document.getElementById("diff_bordador").valueAsNumber;
    var bw = document.getElementById("bw_bordador").checked;


    if( diff == NaN || diff < 0 || diff > 255 || diff == "" || diff == undefined) {
        alert("Por favor insira um núemro válido.");
    }
    else {

        var data = new FormData();
        data.append("file", file)
        data.append("diff", diff)
        data.append("bw", bw)
        
                                
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/bordador");  


        xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
                show_manipulated_image_bordador(JSON.parse( xhr.response ));       //o JSON.parse é essencial para usar a resposta como dicionário, como é pretendido
                }
            };

            xhr.send(data);

        }
}



function show_manipulated_image_bordador(response) {     //mostra a imagem  manipulada; resultado das 2 outros imagens

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "bordador_falhou") {
        let image = document.createElement("img");
        image.src = "../"+response["result"];         //depois de muitas horas a falhar no carregamento da imagem para a página html, mesmo depois de trocar os caminhos de absolutos para relativos (e questionando-me se as imagens afinal estavam no cliente [as do updatePhoto e updatePhoto2 estão] ou no serviDor [como esta, e todas as que se possam buscar através do URL [endereço]]), apercebi-me que a pasta tmp não era dinâmica (essencial para usar os seus conteúdos para alterar cenas no serviDor
        image.width = "550";
        image.height = "450";
        document.getElementById("manipulated_image").appendChild(image);
    }
    else {
        alert("The chosen image could not be altered with Bordador.");
    }
    

    
}


function im_inputs_bordador() {
    //criar input numérico (entre 0 e 255) para o parâmetro "diff"
    var divs = document.createElement("div");
    var textoDiff = document.createElement("input");
    textoDiff.type = "number";
    textoDiff.step = "1";
    textoDiff.min = "0";
    textoDiff.max = "255";
    textoDiff.id = "diff_bordador";
    textoDiff.style="color: blue";

    var labelFator = document.createElement("label");
    labelFator.innerHTML = "Pixel difference (for determining whether the difference between neighbor pixels should be considered enough to border them)";
    labelFator.setAttribute("for", textoDiff.id);


    divs.appendChild(labelFator);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(textoDiff);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(document.createElement("br"));
    divs.appendChild(document.createElement("br"));

    //criar input True or False para o parâmetro "bw"
    var select_bw = document.createElement("input");
    select_bw.type = "checkbox";
    select_bw.value = "on";
    select_bw.id = "bw_bordador";

    var label_bw = document.createElement("label");
    label_bw.innerHTML = "Black and white bordered image, or just contoured image?";
    label_bw.setAttribute("for", select_bw.id);

    divs.appendChild(label_bw);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(select_bw);


    //dar append de ambos ao body da página html
    document.getElementById("other_image").appendChild(divs);
    
}


export {manipulateImage_bordador, sendFile_bordador, show_manipulated_image_bordador, im_inputs_bordador};