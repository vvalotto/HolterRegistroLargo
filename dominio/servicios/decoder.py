def decode_register_channels(register_data, channels_not_decodified):
    zigzag_dec_channels = []
    for page_number in range(len(register_data)):
        zigzag_dec = []
        for data_number in range(0, len(channels_not_decodified[page_number])):    
            data = ((int(channels_not_decodified[page_number][data_number]) >> 1) ^ -(int(channels_not_decodified[page_number][data_number]) & 1))
            if data < 0:
                data = data & 0x0000000000FFFFFF
                data = data*-1 -1
            zigzag_dec.append(data)   
        zigzag_dec_channels.append(zigzag_dec)
        
    #Decodificación delta
    ekg = []
    for page_number in range(len(register_data)):
        delta_dec = []
        for data_number in range(0, len(zigzag_dec_channels[page_number])):
            if(data_number==0):
                delta_dec.append(zigzag_dec_channels[page_number][data_number])
            else:
                delta_dec.append(zigzag_dec_channels[page_number][data_number]+delta_dec[data_number-1])  
        ekg.append(delta_dec)
        
    ch_1 = []
    ch_2 = []
    ch_3 = []

    for page_number in range (int (len(register_data)/3)):
        ch_1 = ch_1 + (list(map(lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ekg [page_number*3])))
        # ch_1 = ch_1 +  ekg[page_number*3]
        ch_2 = ch_2 + (list(map(lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ekg [page_number*3+1])))
        # ch_2 = ch_2 +  ekg [page_number*3+1]
        ch_3 = ch_3 + (list(map(lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ekg [page_number*3+2])))
        # ch_3 = ch_3 +  ekg [page_number*3+2]
    


        # for i in range (len(ekg[page_number*3])):
        #     ch_1.append ((((ekg[page_number*3][i])/0xF30000 - 0.5)*2*2.4/3.5)*1000)



    # ch_1 = list((lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ch_1))
    # ch_2 = list((lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ch_2))
    # ch_3 = list((lambda x: ((x/0xF30000 - 0.5)*2*2.4/3.5)*1000, ch_3))
    # print (type(ch_1))
    # print (len(ch_1))
    # ch_1 = ((ch_1[:]/0xF30000 - 0.5)*2*2.4/3.5)*1000
    # ch_2 = ((ch_1[:]/0xF30000 - 0.5)*2*2.4/3.5)*1000
    # ch_3 = ((ch_1[:]/0xF30000 - 0.5)*2*2.4/3.5)*1000

    return [ch_1, ch_2, ch_3]