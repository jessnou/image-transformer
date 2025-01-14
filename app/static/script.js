let originalImage = null;
let currentImage = null;

document.getElementById("uploadForm").addEventListener("submit", async (event) => {
  event.preventDefault(); // Предотвращаем перезагрузку страницы
  
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image to upload.");
    return;
  }

  // Отображаем предварительный просмотр изображения
  const reader = new FileReader();
  reader.onload = function (e) {
    const previewImage = document.getElementById("previewImage");
    previewImage.src = e.target.result;
    previewImage.style.display = "block"; // Показываем изображение

    originalImage = new Image();
    originalImage.src = e.target.result;
    originalImage.onload = function() {
      currentImage = originalImage;
      document.getElementById("adjustmentSection").style.display = "block"; // Показываем секцию с ползунками
      document.getElementById("filtersSection").style.display = "block"; // Показываем секцию с ползунками
    }
  };
  reader.readAsDataURL(file);
});

document.getElementById("applyAdjustmentsBtn").addEventListener("click", async () => {
  const brightness = document.getElementById("brightness").value;
  const contrast = document.getElementById("contrast").value;
  const saturation = document.getElementById("saturation").value;

  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);
  formData.append("brightness", brightness);
  formData.append("contrast", contrast);
  formData.append("saturation", saturation);

  try {
    const response = await fetch("/apply-adjustments/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to apply adjustments.");
    }

    const result = await response.json();
    displayModifiedImage(result);
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while applying adjustments.");
  }
});

function displayModifiedImage(data) {
  const modifiedImage = document.getElementById("modifiedImage");
  modifiedImage.src = data.modified_image_url;
  document.getElementById("filteredResultSection").style.display = "block"; // Показываем результат изменений
}

document.getElementById("applyFilterBtn").addEventListener("click", async () => {
  const filter = document.getElementById("filterSelect").value;
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image to apply a filter.");
    return;
  }

  // Отправляем изображение на сервер с выбранным фильтром
  const formData = new FormData();
  formData.append("file", file);
  formData.append("filter", filter);

  try {
    const response = await fetch("/apply-filter/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to apply filter.");
    }

    const result = await response.json();
    displayFilteredImage(result);
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while applying the filter.");
  }
});

function displayFilteredImage(data) {
  const filteredImage = document.getElementById("modifiedImage");
  filteredImage.src = data.filtered_image_url;
  document.getElementById("filteredResultSection").style.display = "block"; // Показываем результат фильтрации
}

document.getElementById("applyTransformationsBtn").addEventListener("click", async () => {

  const brightness = Number(document.getElementById("brightness").value);
  const contrast = Number(document.getElementById("contrast").value);
  const saturation = Number(document.getElementById("saturation").value);

  const filter = document.getElementById("filterSelect").value;

  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  const transformations = [
      { type: "filter", filter: filter },
      { type: "adjustments", brightness: brightness, contrast: contrast, saturation: saturation }
  ];

  const formData = new FormData();
  formData.append("file", file);
  formData.append("transformations", JSON.stringify(transformations));

  const response = await fetch("/apply-transformations/", {
      method: "POST",
      body: formData
  });

  const data = await response.json();
  displayFilteredImage(data)
});


document.getElementById("styleTransferForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  
  const formData = new FormData(event.target);

  const response = await fetch("/apply-style-transfer/", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  if (data.styled_image_url) {
    document.getElementById("styledImage").src = data.styled_image_url;
  } else {
    alert("Error: " + data.error);
  }
});
