function manipulateImage_resizer(file) {                       
    if(file != null) {
        sendFile_resizer(file);
    }
    else alert("Image missing!");
}

function sendFile_resizer(file) {
	
    var f = document.getElementById("f_resizer").valueAsNumber;
    
    var modo = document.getElementById("form_mode").elements["modo"].value;


    if( f == NaN || f < 0 || f > 3|| f == "" || f == undefined) {
        alert("Por favor insira um número válido.");
    }
    else {

        var data = new FormData();
        data.append("file", file)
        data.append("f", f)
        data.append("mode", modo)
        
                                
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/resizer");  


        xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
                show_manipulated_image_resizer(JSON.parse( xhr.response ));       //o JSON.parse é essencial para usar a resposta como dicionário, como é pretendido
                }
            };

            xhr.send(data);

        }
}



function show_manipulated_image_resizer(response) {     //mostra a imagem  manipulada; resultado das 2 outros imagens

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "resizer_falhou") {
        let image = document.createElement("img");
        image.src = "../"+response["result"];         //depois de muitas horas a falhar no carregamento da imagem para a página html, mesmo depois de trocar os caminhos de absolutos para relativos (e questionando-me se as imagens afinal estavam no cliente [as do updatePhoto e updatePhoto2 estão] ou no serviDor [como esta, e todas as que se possam buscar através do URL [endereço]]), apercebi-me que a pasta tmp não era dinâmica (essencial para usar os seus conteúdos para alterar cenas no serviDor
        image.width = "550";
        image.height = "450";
        document.getElementById("manipulated_image").appendChild(image);
    }
    else {
        alert("The chosen image could not be altered with resizer.");
    }
    

    
}


function im_inputs_resizer() {
    //criar input numérico (entre 0 e 3) para o parâmetro "diff"
    var divs = document.createElement("div");
    var textoDiff = document.createElement("input");
    textoDiff.type = "number";
    textoDiff.step = "0.1";
    textoDiff.min = "0";
    textoDiff.max = "3";
    textoDiff.id = "f_resizer";
    textoDiff.style="color: blue";

    var labelFator = document.createElement("label");
    labelFator.innerHTML = "Resize factor (0 < f < 3)";
    labelFator.setAttribute("for", textoDiff.id);


    divs.appendChild(labelFator);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(textoDiff);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(document.createElement("br"));
    divs.appendChild(document.createElement("br"));

    //criar inputs radio para cada 1 dos 4 modos possíveis
    //nearest
    //var divNearest = document.createElement("div");

    var form = document.createElement("form");
    form.id = "form_mode";

    var select_mode_nearest = document.createElement("input");
    select_mode_nearest.type = "radio";
    select_mode_nearest.name = "modo";                          //para que os butões pertençam ao mesmo grupo (isto é, ao selecionar um, descelecionam-se os outros), dá-se o mesmo "name" aos que queremos que assim se comportem
    select_mode_nearest.value = "nearest";
    select_mode_nearest.id = "modo_nearest";
    select_mode_nearest.checked = true;                            //queremos que esteja  um valor checked para dar o submit

    var label_select_mode_nearest = document.createElement("label");
    label_select_mode_nearest.innerHTML = "Nearest  ";
    label_select_mode_nearest.setAttribute("for", select_mode_nearest.id);

    //bilinear
    //var divBilinear = document.createElement("div");
    var select_mode_bilinear = document.createElement("input");
    select_mode_bilinear.type = "radio";
    select_mode_bilinear.name = "modo";
    select_mode_bilinear.value = "bilinear";
    select_mode_bilinear.id = "modo_bilinear";

    var label_select_mode_bilinear = document.createElement("label");
    label_select_mode_bilinear.innerHTML = "Bilinear"; 
    label_select_mode_bilinear.setAttribute("for", select_mode_bilinear.id);

    //bicubic
    //var divBicubic = document.createElement("div");
    var select_mode_bicubic = document.createElement("input");
    select_mode_bicubic.type = "radio";
    select_mode_bicubic.name = "modo";
    select_mode_bicubic.value = "bicubic";
    select_mode_bicubic.id = "modo_bicubic";

    var label_select_mode_bicubic = document.createElement("label");
    label_select_mode_bicubic.innerHTML = "Bicubic ";
    label_select_mode_bicubic.setAttribute("for", select_mode_bicubic.id);

    //antialias
    //var divAntialias = document.createElement("div");
    var select_mode_antialias = document.createElement("input");
    select_mode_antialias.type = "radio";
    select_mode_antialias.name = "modo";
    select_mode_antialias.value = "antialias";
    select_mode_antialias.id = "modo_antialias";

    var label_select_mode_antialias = document.createElement("label");
    label_select_mode_antialias.innerHTML = "Antialias";
    label_select_mode_antialias.setAttribute("for", select_mode_antialias.id);


    form.appendChild(label_select_mode_nearest);
    form.appendChild(select_mode_nearest);
    form.appendChild(document.createElement("br"));    

    form.appendChild(label_select_mode_bilinear);
    form.appendChild(select_mode_bilinear);
    form.appendChild(document.createElement("br"));    

    form.appendChild(label_select_mode_bicubic);
    form.appendChild(select_mode_bicubic);
    form.appendChild(document.createElement("br"));    

    form.appendChild(label_select_mode_antialias);
    form.appendChild(select_mode_antialias);

    divs.appendChild(form);

    //divNearest.appendChild(label_select_mode_nearest);
    //divBilinear.appendChild(label_select_mode_bilinear);
    //divBicubic.appendChild(label_select_mode_bicubic);
    //divAntialias.appendChild(label_select_mode_antialias);


    //divNearest.appendChild(select_mode_nearest);    
    //divBilinear.appendChild(select_mode_bilinear);
    //divBicubic.appendChild(select_mode_bicubic);
    //divAntialias.appendChild(select_mode_antialias);

    //divs.appendChild(divNearest);
    //divs.appendChild(divBilinear);
    //divs.appendChild(divBicubic);
    //divs.appendChild(divAntialias);

    //dar append de ambos ao body da página html
    document.getElementById("other_image").appendChild(divs);
    
}


export {manipulateImage_resizer, sendFile_resizer, show_manipulated_image_resizer, im_inputs_resizer};