import cv2
import tensorflow as tf

# Загрузка модели
model = tf.keras.models.load_model(r"coastalassistance\neural_networks\model_beach")


async def check_prediction(image_path):
    test_img = cv2.imread(image_path)
    print("Размер изображения:", test_img.shape)

    test_img = cv2.resize(test_img, (150, 150))
    test_input = test_img.reshape((1, 150, 150, 3))

    # Получение предсказания
    prediction = model.predict(test_input)
    print("Результат предсказания:", prediction)

    # Проверяем, если вероятность предсказания больше 20%
    if prediction > 0.2:
        return True
    else:
        return False
