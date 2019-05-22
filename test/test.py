# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''
path = os.getcwd() + '/app/utils/AI_face_beauty'

image = request.files.get('image')
save_path = path + '/temp/' + 'face.jpg'
image.save(save_path)

result = faceIdentity(save_path)