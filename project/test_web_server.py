import pytest                                        #usa-se o comando "py.test-3" para correr estes testes de python
import imagem_modificador                    
        

 #inputs para a função watermark: imagename1, imagename2, transparency_factor, start_x, start_y
def test_watermark_f():

    #teste com parâmetro de transparência inválido
    result = imagem_modificador.watermark("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", "uploads/d519f06f6f1e5a0f2625d19ffb741697da66c522de4ff38a6f542375c4b4ddb1.jpg", "letra", 0, 0)
    expected_error = "watermark_falhou"
    assert(result == expected_error)


def test_watermark_filename2():
    #teste com parâmetro de segunda imagem errado
    result = imagem_modificador.watermark("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", 29, 0.2, 0, 0)
    expected_error = "watermark_falhou"
    assert(result == expected_error)


def test_watermark_x_y():
    #teste com parâmetros de posição da watermark que saiem fora da imagem original
    result = imagem_modificador.watermark("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", "uploads/d519f06f6f1e5a0f2625d19ffb741697da66c522de4ff38a6f542375c4b4ddb1.jpg", 0.2, 1000, 1000)
    expected_error = "watermark_falhou"
    assert(result == expected_error)


def test_watermark():
    #teste com parâmetros válidos (a imagem resultante fica na pasta tmp; as 2 imagens original e watermark só são reescritas na mesma pasta onde estão, que é ./uploads, quando esta função é chamada na função watermark da app.py)
    result = imagem_modificador.watermark("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", "uploads/d519f06f6f1e5a0f2625d19ffb741697da66c522de4ff38a6f542375c4b4ddb1.jpg", 0.2, 0, 0)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de vignette: imagename1, x_ref, y_ref
def test_vignette_filename():
    #teste com nome de imagem inválido
    result = imagem_modificador.vignette("dor", 0, 0)
    expected_error = "vignette_falhou"
    assert(result == expected_error)


def test_vignette_x_y():
    #teste com parâmetros posicionais errados
    result = imagem_modificador.vignette("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", -1000, "a")
    expected_error = "vignette_falhou"
    assert(result == expected_error)


def test_vignette():
    #teste com parâmetros válidos
    result = imagem_modificador.vignette("uploads/0495574b3b6221ce0af9d9df45571df603c2c5981ccc95d59c924c8779fe2ca5.jpg", 700, 700)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)


#inputs de bordador: fname, diff, bw
def test_bordador_filename():
    #teste com nome de imagem inválido
    result = imagem_modificador.im_handler(23, 0, 0)
    expected_error = "bordador_falhou"
    assert(result == expected_error)


def test_bordador_diff():
    #teste com parâmetro de diff inválido
    result = imagem_modificador.im_handler("images/img.jpg", "256", False)
    expected_error = "bordador_falhou"
    assert(result == expected_error)


def test_bordador():
    #teste com parâmetros válidos
    result = imagem_modificador.im_handler("images/img.jpg", 40, False)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de sepia: imagename
def test_sepia_imagename():
    #teste com parâmetro de nome de imagem inválido
    result = imagem_modificador.sepia(0)
    expected_error = "sepia_lomografia_falhou"
    assert(result == expected_error)


def test_sepia():
    #teste com parâmetros válidos
    result = imagem_modificador.sepia("images/img.jpg")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de lomografia: imagename
def test_lomografia_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.lomografia("0")
    expected_error = "sepia_lomografia_falhou"
    assert(result == expected_error)


def test_lomografia():
    #teste com parâmetros válidos
    result = imagem_modificador.lomografia("images/img.jpg")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de saturation: imagename, fator_de_saturação
def test_saturation_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.saturation("0", 0)
    expected_error = "saturador_falhou"
    assert(result == expected_error)


def test_saturation_f():
    #teste com parâmetro de fator inválido
    with pytest.raises(SystemExit) as e:
        imagem_modificador.saturation("images/img.jpg", "1a")
    assert e.type == SystemExit
    assert e.value.code == 29


def test_saturation():
    #teste com parâmetros válidos
    result = imagem_modificador.saturation("images/img.jpg", 2)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de gamma: imagename, fator_de_gamma
def test_gamma_modificaDor_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.gamma_modificaDor("0", 0)
    expected_error = "gamma_falhou"
    assert(result == expected_error)


def test_gamma_modificaDor_g():
    #teste com parâmetro de fator inválido
    with pytest.raises(SystemExit) as e:
        imagem_modificador.gamma_modificaDor("images/img.jpg", "1a")
    assert e.type == SystemExit
    assert e.value.code == -29


def test_gamma_modificaDor():
    #teste com parâmetros válidos
    result = imagem_modificador.gamma_modificaDor("images/img.jpg", 2)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de image_modifier_intensifier: imagename, fator_de_intensidade
def test_image_modifier_intensifier_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.image_modifier_intensifier("0", 0)
    expected_error = "intensificador_falhou"
    assert(result == expected_error)


def test_image_modifier_intensifier_f():
    #teste com parâmetro de fator inválido
    result = imagem_modificador.image_modifier_intensifier("images/img.jpg", "a")
    expected_error = "intensificador_falhou"
    assert(result == expected_error)


def test_image_modifier_intensifier():
    #teste com parâmetros válidos
    result = imagem_modificador.image_modifier_intensifier("images/img.jpg", 2)
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)



#inputs de cinza: imagename
def test_image_modifier_cinza_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.image_modifier_cinza("0")
    expected_error = "unknown_falhou"
    assert(result == expected_error)


def test_image_modifier_cinza():
    #teste com parâmetro válido
    result = imagem_modificador.image_modifier_cinza("images/img.jpg")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)




#inputs de imagem_negativa: imagename
def test_imagem_negativa_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.imagem_negativa("0")
    expected_error = "unknown_falhou"
    assert(result == expected_error)


def test_imagem_negativa_cinza():
    #teste com parâmetro válido
    result = imagem_modificador.imagem_negativa("images/img.jpg")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)




#inputs de trocar_canais_red_green: imagename
def test_trocar_canais_red_green_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.trocar_canais_red_green("a")
    expected_error = "unknown_falhou"
    assert(result == expected_error)


def test_trocar_canais_red_green():
    #teste com parâmetro válido
    result = imagem_modificador.trocar_canais_red_green("images/img.jpg")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)





#inputs de resizer: imagename, tamanho, modo
def test_resizer_imagename():
    #teste com parâmetro de caminho de imagem inválido
    result = imagem_modificador.resizer("a", 1.5, 'bilinear')
    expected_error = "resizer_falhou"
    assert(result == expected_error)


def test_resizer_tamanho():
    #teste com parâmetro de tamanho inválido
    with pytest.raises(SystemExit) as e:
        imagem_modificador.resizer("images/img.jpg", "1.5a", 'bicubic')
    assert e.type == SystemExit


def test_resizer():
    #teste com parâmetro válido
    result = imagem_modificador.resizer("images/img.jpg", 1.5, "alguma coisa")
    expected_result_start = "tmp/"
    assert(result[0:4] == expected_result_start)
