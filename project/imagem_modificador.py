from PIL import Image, ImageDraw, ImageFont
import sys, math, time, os





#18) meter imagem (watermark) noutra imagem
def watermark_positions(fname1, fname2):
    try:
        im = Image.open(fname1)
        width, height = im.size

        im2 = Image.open(fname2)
        width2, height2 = im2.size
    except:
        print("Não foi possível abrir os ficheiros através do PIL.Image.")
        return (None, None)
    

    x_start=width-width2            #para colocar as watermarks no canto inferior esquerdo, inteiras e com as suas bordas direita e inferior a coincidar com as bordas direita e inferior da imagem original
    y_start=height-height2

    if (x_start < 0) or (y_start < 0):
        print("Não é possível meter a imagem2 na imagem1 sem que ocorra overlap.")
        return (None, None) 

    return (x_start, y_start)



def watermark(fname1, fname2, f, start_x, start_y):

    try:
        im = Image.open(fname1)
        
    
        new_im = im


        im_water = Image.open(fname2)
        im_water = im_water.convert("RGBA")
        width_water, height_water = im_water.size
    except:
        print("Erro ao abrir imagens.")
        return "watermark_falhou" 
   
    
    try:
        for x in range(width_water ):
            for y in range(height_water ):
    

                #p1 é um pixel da imagem original
                #p2 é um pixel da marca de água
                p1 = im.getpixel( (x+start_x, y+start_y) )
                p2 = im_water.getpixel( (x,y) )
                if(p2[3] == 0):
                    continue

                r = int(p1[0]*(1-f)+p2[0]*f)
                g = int(p1[1]*(1-f)+p2[1]*f)
                b = int(p1[2]*(1-f)+p2[2]*f)


                new_im.putpixel( (x+start_x, y+start_y), (r, g, b) )        #faltava mudar (x,y) para (x+start_x, y+start_y) para que a marca de água fosse adicionada ao canto inferior direito, em vez de o canto superior esquerdo como táva a ocorrer e eu não sabia porquê
    except:
        print("A colocação da watermark na imagem original falhou.")
        return "watermark_falhou"

    #new_im.save(fname1+"-watermark-"+".png")    #tive que alterar para .png, embora funcionasse bem para .jpg no terminal. Edit: adicionei um datetime para resolver os problemas de cache
    
    
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname1)
    new_im_name = "tmp/"+tail+"-watermark-"+datetime+".png"

    new_im.save(new_im_name)    #tive que alterar para .png, embora funcionasse bem para .jpg no terminal. Edit: adicionei um datetime para resolver os problemas de cache
    return new_im_name








#17) vignette
def get_factor(x, y, xref, yref):
    distance = math.sqrt( pow(x-xref,2) + pow(y-yref,2))
    distance_to_edge = math.sqrt( pow(xref,2) + pow(yref,2))
    return 1-(distance/distance_to_edge) #Percentagem


def vignette_positions(fname):
    im = Image.open(fname)
    width, height = im.size
    xref=width/2
    yref=height/2
    return (xref, yref)


def vignette(fname, xref, yref):

    try:
        im = Image.open(fname)
        
        width, height = im.size

        new_im = Image.new(im.mode, im.size)


        for x in range(width):
            for y in range(height):
                p = im.getpixel( (x,y) )

                f = get_factor(x,y,xref,yref)
                p_r = int(p[0] * f)
                p_g = int(p[1] * f)
                p_b = int(p[2] * f)

                new_im.putpixel( (x,y), (p_r, p_g, p_b) )
    except:
        print("Erro ao abrir imagem e aplicar vignette com centro no ponto desejado.")
        return "vignette_falhou"


    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-vignette-"+datetime+".png"

    new_im.save(new_im_name)
    return new_im_name









#16) bordador
def is_edge(im, x,y, diff, bw):
    #Obter o pixel
    p = im.getpixel( (x , y) )
    width, height = im.size

    if x < width-1 and y < height-1 and x > 0 and y > 0:

        #Vizinhos acima e abaixo
        for vx in range(-1,1):
            for vy in [-1, 1]:
                px = im.getpixel( (x + vx, y + vy) )
                if abs(p[0]- px[0]) > diff:
                    return (0,128,128)
            
        #Vizinhos da esquerda e direita
        for vx in [-1, 1]:
            px = im.getpixel( (x + vx, y) )
            if abs(p[0]- px[0]) > diff:
                return (0,128,128)
            
        if bw :
            return (255,128,128)
        else:
            return p
        


def iterativaDor(im, new_im, diff, bw):
    width, height = im.size
    for vx in range(1,width-1):
        for vy in range(1,height-1):
            p_dor = is_edge(im, vx, vy, diff, bw)
            #if p_dor:
            new_im.putpixel( (vx, vy), p_dor)



def im_handler(fname, diff, bw):

    try:
        im=Image.open(fname)

        new_im=Image.new(im.mode, im.size)
        #recursivaDor(im, new_im, 1, 1, diff, bw)     #os pixeis de borda não são elegíveis, pelo que se deve começar no (1,1)
        iterativaDor(im, new_im, diff, bw)
    except:
        print("Erro ao abrir imagem ou colocar as bordas nela.")
        return "bordador_falhou"

    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-bordaDor-"+datetime+".png"

    new_im.save(new_im_name)
    return new_im_name








#15) sepia e lomografia
def sepia(fname):

    try:
        im = Image.open(fname)
        
        width, height = im.size

        new_im = Image.new(im.mode, im.size)


        for x in range(width):
            for y in range(height):
                p = im.getpixel( (x,y) )

                r = p[0]
                b = p[1]
                g = p[2]

                r1 = int(0.189*r + 0.769*g + 0.393*b)
                g1 = int(0.168*r + 0.686*g + 0.349*b)
                b1 = int(0.131*r + 0.534*g + 0.272*b)

                new_im.putpixel( (x,y), (r1, g1, b1) )
    except:
        print("Erro ao abrir imagem e aplicar sepia.")
        return "sepia_lomografia_falhou"

    #new_im.save(fname+"-sepia-"+".jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-sepia-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name




def lomografia(fname):

    try:
        im = Image.open(fname)
        width, height = im.size
        new_im = Image.new(im.mode, im.size)


        for x in range(width):
            for y in range(height):
                p = im.getpixel( (x,y) )

                r = p[0]
                b = p[1]
                g = p[2]

                r1 = min(255, int(0.189*r + 0.769*g + 0.393*b))
                g1 = min(255, int(0.168*r + 0.686*g + 0.349*b))
                b1 = min(255, int(0.131*r + 0.534*g + 0.272*b))

                new_im.putpixel( (x,y), (r1, b1, g1) )
    except:
        print("Erro ao abrir imagem e aplicar lomografia.")
        return "sepia_lomografia_falhou"

    #new_im.save(fname+"-lomografia-"+".jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-lomografia-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name







#14) saturation
def saturation(fname, f):
    try:
        f=float(f)
    except:
        print("Por favor, insira como 2º argumento um número válido.")
        exit(29)


    try:
        im = Image.open(fname)
        
        width, height = im.size

        new_im = im.convert("YCbCr")


        for x in range(width):
            for y in range(height):
                p = new_im.getpixel( (x,y) )
                py = p[0] # [0] is the Y channel
                pb = min(255,int((p[1] - 128) * f) + 128)
                pr = min(255,int((p[2] - 128) * f) + 128)

                new_im.putpixel( (x,y), (py, pb, pr) )
    except:
        print("Erro ao abrir imagem e aplicar saturação.")
        return "saturador_falhou"

    #new_im.save(fname+"-saturation-"+str(f)+".jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-saturation-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name






#13) gammaficador
def gamma_modificaDor(fname, g):
    try:
        g=float(g)
    except:
        print("Por favor, insira como 2º argumento um número válido.")
        exit(-29)

    try:
        im = Image.open(fname)
        
        width, height = im.size

        new_im = im.convert("YCbCr")

        f=255/(255**g)

        for x in range(width):
            for y in range(height):
                pixel = new_im.getpixel( (x,y) )
                py = min(255, int(pixel[0]**g * f)) # [0] is the Y channel
                new_im.putpixel( (x,y), (py, pixel[1], pixel[2]) )
    except:
        print("Erro ao abrir imagem e aplicar gamma.")
        return "gamma_falhou"

    #new_im.save(fname+"-gamma_modificaDor-"+str(g)+".jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-gamma_modificaDor-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name








#12) intensificador
def image_modifier_intensifier(fname, f):
    try:
        f=float(f)
    except:
        print("Por favor, insira como 2º argumento um número válido.")

    try:
        im = Image.open(fname)
        new_im = intensifier(im, f)
    except:
        print("Erro ao abrir imagem e aplicar intensificador.")
        return "intensificador_falhou"
    #new_im.save(fname+"-intensidade-"+str(f)+".jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-intensificador-"+str(f)+"-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name


def intensifier(im, f):
    width, height = im.size
    new_im = im.convert("YCbCr")
    width, height = im.size

    for x in range(width):
        for y in range(height):
            pixel = new_im.getpixel( (x,y) )
            py = min(255, int(pixel[0] * f)) # [0] is the Y channel
            new_im.putpixel( (x,y), (py, pixel[1], pixel[2]) )

    return new_im






#11) cinza
def image_modifier_cinza(fname):
    try:
        im = Image.open(fname)
        new_im = effect_gray(im)
    except:
        print("Erro ao abrir imagem e aplicar cinza.")
        return "unknown_falhou"
    #new_im.save(fname+"-cinza.jpg")

    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-cinza-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name


def effect_gray(im):
    width, height = im.size
    new_im = Image.new("L", im.size)

    for x in range(width):
        for y in range(height):
            p = im.getpixel( (x,y) )
            l = int(p[0]*0.29 + p[1]*0.1 + p[2]*0.1996)
            new_im.putpixel( (x,y), (l) )

    return new_im








#10) negativificador
def imagem_negativa(fname):

    try:
        im = Image.open(fname)
        new_im = Image.new(im.mode, im.size)
        width, height = im.size


        for x in range(width):
            for y in range(height):
                p = im.getpixel( (x,y) )
                r = 255-p[0]
                g = 255-p[1]
                b = 255-p[2]
                new_im.putpixel((x,y), (r, g, b) )
    except:
        print("Erro ao abrir imagem e torná-la negativa.")
        return "unknown_falhou"


    #new_im.save(fname+"-negative-image.jpg")        #demorei algum tempo até perceber porque é que a imagem criada não tinha grandes diferenças da original, que se devia a esta linha; eu tinha "im.save()", em que im tem os dados da imagem original, em vez de "new_im.save()", que tem os novos dados
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-negativador-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name




#9) trocar_channel_red_green
def trocar_canais_red_green(fname):
    try:
        im = Image.open(fname)
        new_im = Image.new(im.mode, im.size)
        width, height = im.size

        for x in range(width):
            for y in range(height):
                p = im.getpixel( (x,y) )
                r = p[1]
                g = p[0]
                b = p[2]
                new_im.putpixel((x,y), (r, g, b) )
    except:
        print("Erro ao abrir imagem e trocar canais vermelho e verde.")
        return "unknown_falhou"

    #new_im.save(fname+"-trocados-canais-red-green.jpg")
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-trocados-canais-red-green-"+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name





#5) desqualificador
def desqualificador(fname, quality):

    try:
        quality = float(quality)
    except:
        print("Por favor insira uma qualidade válida.")
        exit()


    im = Image.open(fname)
    #im.save(fname+"-qualidade-"+str(quality)+".jpg", quality=quality)
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+"-qualidade-"+str(quality)+datetime+".jpg"

    im.save(new_im_name)
    return new_im_name




#2) antialiase, nearest, bilinear bicubic
def resizer(fname, tamanho, modo):

    try:
        tamanho=float(tamanho)
    except:
        print("Por favor insira um tamanho válido.")
        exit()

    try:
        im = Image.open(fname)

        width, height = im.size
        dimension = ( int(width*tamanho), int(height*tamanho) )

    
        if modo.lower() == 'bilinear':
            new_im = im.resize( dimension, Image.BILINEAR)
        elif modo.lower() == "bicubic":
            new_im = im.resize( dimension, Image.BICUBIC)
        elif modo.lower() == "antialias":
            new_im = im.resize( dimension, Image.ANTIALIAS)
        else:
            new_im = im.resize( dimension, Image.NEAREST)
    except:
        print("Erro ao abrir imagem e aplicar método de resize.")
        return "resizer_falhou"

    #new_im.save(fname+"-%.2f.jpg" % tamanho)
    datetime = str(time.time_ns()//1000)

    head, tail = os.path.split(fname)
    new_im_name = "tmp/"+tail+str(tamanho)+modo+datetime+".jpg"

    new_im.save(new_im_name)
    return new_im_name









