//updatePhoto -> apresenta na página html a imagem selecionada pelo utilizador no "input" de imagem no "canvas" respetivo (o "input" e o "canvas" já estão presentes na página html, esta função preenche o "canvas" com os dados/imagem escolhido no "input")
//im_watermark -> cria um "div", "canvas", e um "input" de imagem e dá-lhes append num "div" debaixo do "div" (inicialmente vazio) com id="photo" (que já está presente), e "input" de texto para o fator de transparência (nenhum destes elementos está presenta na página html quando é carregada). Quando se escolhe uma imagem no "input" de imagem criado, chama-se a função "updatePhoto2"
//updatePhoto2 -> função semelhante a updatePhoto, mas que apresenta a imagem selecionada pelo utilizador no "input" de imagem criado pela função "im_watermark", no "canvas" criado pela mesma função, que está no "div" criado pela mesma função, que é appended no "div" inicialmente vazio da página html, abaixo do "div" da iamgem original
//sendFile_watermark -> envia um request /POST ao servidor, com os dados das 2 imagens escolhidas pelo utilizador, bem como o valor do fator de transparência escrito pelo utilizador no "input" de texto. Após o envio do /POST, é invocada a função "updateProgress" para sinalizar o envio total dos dados, e após tal, a função espera pela resposta do servidor, e caso esta indique sucesso por parte do servidor, invoca a "show_manipulated_image"
//show_manipulated_image -> lê a resposta do servidor (que é um parâmetro de entrada nesta função), e caso a resposta contenha o caminho relativo da imagem resultante da manipulação das 2 imagens previamente selecionadas e carregadas para variáveis com as funções "updatePhto" e "updatePhoto2", enviadas pelo "sendFile_watermark", cria e mostra essa imagem (que se encontra na pasta tmp/ do servidor, e as 2 imagens selecionadas pelo utilizador, estavam no computador do mesmo, mas após o envio do /POST, também são guardadas na tmp/ do servidor) num "div" já existente de início na página html (neste caso, não é criado um "canvas")

import {updatePhoto, im_watermark, updatePhoto2, manipulateImage_watermark, sendFile_watermark, updateProgress, show_manipulated_image, tmp_cleaner } from './image_manipulation_watermark.js';
import {manipulateImage_vignette, sendFile_vignette, show_manipulated_image_vignette} from './image_manipulation_vignette.js';
import {manipulateImage_bordador, sendFile_bordador, show_manipulated_image_bordador, im_inputs_bordador} from './image_manipulation_bordador.js';
import {manipulateImage_sepia_lomografia, sendFile_sepia_lomografia, show_manipulated_image_sepia_lomografia, im_inputs_sepia_lomografia} from './image_manipulation_sepia_lomografia.js';
import {manipulateImage_saturador, sendFile_saturador, show_manipulated_image_saturador, im_inputs_saturador} from './image_manipulation_saturador.js';
import {manipulateImage_gamma, sendFile_gamma, show_manipulated_image_gamma, im_inputs_gamma} from './image_manipulation_gamma.js';
import {manipulateImage_intensificador, sendFile_intensificador, show_manipulated_image_intensificador, im_inputs_intensificador} from './image_manipulation_intensificador.js';
import {manipulateImage_resizer, sendFile_resizer, show_manipulated_image_resizer, im_inputs_resizer} from './image_manipulation_resizer.js';
import {manipulateImage_unknown, sendFile_unknown, show_manipulated_image_unknown} from './image_manipulation_unknown.js';

var file;
window.handler_updatePhoto = function handler_updatePhoto(event) {
    file = updatePhoto(event);
}


window.handler_tmp_cleaner = function handler_tmp_cleaner() {
    tmp_cleaner();
}







window.handler_im_modificador = function handler_im_modificador(event) {        //chamado quando se seleciona uma modificação da lista
    
    var modificador = document.getElementById("algo").value;
    $("#other_image").empty();        //também limpa as cenas da div da da 2ª imagem, para evitar acumulador
    $("#manipulated_image").empty();    //limpar o div onde fica a imagem manipulada
    if (modificador == "Watermark") im_watermark();
    //if (modificador == "Vignette") im_vignette();
    if (modificador == "Bordador") im_inputs_bordador();
    if (modificador == "Sepsis/Lomography") im_inputs_sepia_lomografia();
    if (modificador == "Saturation") im_inputs_saturador();
    if (modificador == "Gamma") im_inputs_gamma();
    if (modificador == "Intensifier") im_inputs_intensificador();
    if (modificador == "Resizer") im_inputs_resizer();
}



window.handler_manipulateImage = function handler_manipulateImage() { //chamado quando se clica no botão Manipulate
    
    var manipulation = document.getElementById("algo").value;
    //alert(manipulation)
    if (manipulation == "Watermark") manipulateImage_watermark()
    if (manipulation == "Vignette") manipulateImage_vignette(file)   //o watermark utiliza uma variável file declarada dentro do .js onde está definida, mas o .js do vignette não tem essa variável, nem o uploadPhoto para a preencher. Temos que usar o updatePhoto de modo a que este retorne os dados da imagem, de modo a que possam ser usados como argumento desta função
    if (manipulation == "Bordador") manipulateImage_bordador(file)
    if (manipulation == "Sepsis/Lomography") manipulateImage_sepia_lomografia(file)
    if (manipulation == "Saturation") manipulateImage_saturador(file);
    if (manipulation == "Gamma") manipulateImage_gamma(file);
    if (manipulation == "Intensifier") manipulateImage_intensificador(file);
    if (manipulation == "Resizer") manipulateImage_resizer(file);
    if (manipulation == "Unknown") manipulateImage_unknown(file);
}