
# 📘 API Endpoint Documentation

Bu API, kıyafet görselleri üzerinde arka plan silme, iyileştirme (enhance), düzenleme (edit) ve açıklama oluşturma (caption) işlemlerini yönetir.

---

### 🔗 `POST /chain/process`

**Açıklama:** Görseli Supabase’a yükler, enhance ve/veya rembg işlemini arka planda başlatır.

**Input (Form Data):**

* `user_id` (string)
* `clothe_image` (file)
* `category` (string)
* `is_long_top` (boolean)
* `is_enhance` (boolean)

**Response:**

```json
{
  "job_id": "..."
}
```

---

### 🔎 `GET /chain/job-status/{job_id}/{is_enhance}`

**Açıklama:** İlgili zincir işleminin (enhance/rembg) güncel durumunu verir.

**Path Params:**

* `job_id` (string)
* `is_enhance` (boolean)

**Response:**

```json
{
  "job_id": "...",
  "status": "processing" | "finished" | "failed",
  "result_url": "..." // yalnızca tamamlandıysa
}
```

---

### 🪄 `POST /replicate/late-enhance`

**Açıklama:** Var olan bir görsel için geç (late) bir enhance/rembg/caption işlemi başlatır.

**Input (Form Data):**

* `user_id` (string)
* `image_url` (string)
* `is_enhance` (boolean)
* `wardrobe_id` (string)

**Response:**

```json
{
  "job_id": "..."
}
```

---

### 🔁 `GET /late-enhance/job-status/{job_id}/{is_enhance}`

**Açıklama:** Geç başlatılan işlemin durumunu döner.

**Path Params:**

* `job_id` (string)
* `is_enhance` (boolean)

**Response:**

```json
{
  "job_id": "...",
  "status": "processing" | "finished" | "failed",
  "result_url": "..." // yalnızca tamamlandıysa
}
```

---

### 🧠 `POST /webhook/replicate-enhance`

**Açıklama:** Enhance işlemi tamamlandığında tetiklenir, ardından rembg başlatılır.

**Input:** Replicate webhook JSON payload
**Response:**

```json
{
  "status": "Enhance webhook received successfully, and rembg started"
}
```

---

### 🧠 `POST /webhook/late-enhance`

**Açıklama:** Geç başlayan enhance işlemi tamamlandığında zincirin devamını tetikler.

**Input:** Replicate webhook JSON payload
**Response:**

```json
{
  "status": "Enhance webhook received successfully, and rembg started"
}
```

---

### 🧠 `POST /webhook/replicate/fast-rembg`

**Açıklama:** Background removal işlemi tamamlandığında sonucu sisteme işler.

**Input:** Replicate webhook JSON payload
**Response:**

```json
{
  "status": "Webhook rembg received successfully"
}
```

---

### 🧠 `POST /webhook/image-edit`

**Açıklama:** Görsel düzenleme işlemi tamamlandığında sonucu işler.

**Input:** Replicate webhook JSON payload
**Response:**

```json
{
  "status": "Edit webhook received successfully"
}
```

---

### 🎨 `POST /replicate/image-edit`

**Açıklama:** Bir görsele verilen prompt’a göre düzenleme başlatır.

**Input (Form Data):**

* `user_id` (string)
* `image` (file)
* `prompt` (string)

**Response:**

```json
{
  "job_id": "..."
}
```

---

### 📊 `GET /edit/job-status/{job_id}`

**Açıklama:** Düzenleme işleminin güncel durumunu verir.

**Path Params:**

* `job_id` (string)

**Response:**

```json
{
  "job_id": "...",
  "status": "processing" | "finished" | "failed",
  "result_url": "..." // yalnızca tamamlandıysa
}
```
