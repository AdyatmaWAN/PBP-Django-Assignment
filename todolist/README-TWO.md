PBP Tugas 6
=
### Adyatma Wijaksara Aryaputra Nugraha Yudha - 2106750805
### [Web Page](https://pbp-tugas2-adyatma.herokuapp.com/todolist)
Jelaskan perbedaan antara asynchronous programming dengan synchronous programming.
-
Asynchronous programming adalah sebuah teknik yang digunakan untuk menjalankan sebuah program secara bersamaan dengan program lainnya. Synchronous programming adalah sebuah teknik yang digunakan untuk menjalankan sebuah program secara berurutan dengan program lainnya.

Dalam penerapan JavaScript dan AJAX, terdapat penerapan paradigma Event-Driven Programming. Jelaskan maksud dari paradigma tersebut dan sebutkan salah satu contoh penerapannya pada tugas ini.
-
Paradigma Event-Driven Programming adalah sebuah paradigma yang digunakan untuk mengatur sebuah program agar dapat berjalan berdasarakan event atau tindakan pengguna atau pesan dari program lain. 

Contoh penerapannya pada tugas ini adalah ketika pengguna menekan tombol "Create New Task" maka akan terjadi sebuah event yang akan memanggil modal berisi form. Lalu ketika form sudah terisi dan tombol "Submit" ditekan, maka akan terjadi sebuah event yang akan memanggil fungsi untuk menambahkan task baru ke dalam database dan menampilkannya ke page.

Jelaskan penerapan asynchronous programming pada AJAX.
-
1. Tambahkan `<script>` yang berisi program JavaScript
2. Tambahkan library AJAX <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
3. Tambahkan program AJAX dalam `<script>` yang telah dibuat pada langkah 1
4. Ketika terdapat event dan server request, event dan server request akan diproses AJAX
5. AJAX akan melakukan transfer data berdasarkan event dan server request, dan diproses secara server-side
6. Hasil proses data akan ditampilkan pada page secara asynchronous tanpa harus reload page

Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
-
1. Buat fungsi di `views.py` untuk menampilkan data dari database dan menyimpan data ke dalam database
```
@login_required(login_url="/todolist/login")
def show_todolist_json(request):
    tasks = TodoListItems.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', tasks), content_type='application/json')

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        new_task = TodoListItems(user=request.user, title=title, description=description, date=datetime.now())
        new_task.save()
        return HttpResponse(b"CREATED", status=20)
    return HttpResponseNotFound()
```
2. Buat url routing pada `urls.py` memanggil fungsi di `views.py`
```
path('show_todolist_json', views.show_todolist_json, name='show_todolist_json'),
path('add_task/', add_task, name='add_task'),

```
3. Membuat template `alt-todolist.html` baru untuk template penerapan AJAX
4. Menambahkan library AJAX pada `base.html`
```  
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
```
5. Membuat tabel untuk menampilkan data dari database (`id = 'content'`)
```
<div class="w-80 d-flex">
        <table class="table table-striped ">
            <thead>
                <tr class="">
                    <th class="text-center" scope="col">TodoList</th>
                </tr>
            </thead>
            <tbody id="content"></tbody>
        </table>
    </div>
```
6. Membuat modal untuk menambahkan task baru

Pemanggilan modal
```
<div class="d-flex justify-content-center mt-5">
        <a class="btn btn-outline-secondary " data-bs-toggle="modal" data-bs-target="#modal-ajax">Create New Task</a>
</div>
```
Modal
```
<div class="modal fade" id="modal-ajax" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Add Task</h1>
                    <button type="button" class="btn" data-bs-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="form" method="POST">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="title" class="col-form-label">Title</label>
                            <input type="text" name="title" class="form-control" id="title" required>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="col-form-label">Description</label>
                            <textarea class="form-control" id="description"  name="description" required></textarea>
                        </div>

                        <input type="submit" id="submit-modal" class="btn btn-primary" data-bs-dismiss="modal"></input>
                    </form>
                </div>
            </div>
        </div>
    </div>
```
7. Menambahkan fungsi JavaScript pada `alt-todolist.html` untuk fetch data dari database dan menampilkannya ke page

`fetch` 
```
async function getTask() {
            return fetch("{% url 'todolist:show_todolist_json' %}").then((response) => response.json());
        }
```
`displayTask`
```
async function refreshTask() {
            document.getElementById("content").innerHTML = "";
            const task = await getTask();
            const content = document.getElementById("content");
            content.innerHTML = "";
            task.forEach((item) => {
                let message = ''
                if (item.is_finished){
                    message = 'Completed'
                } else {
                    message = 'Incomplete'
                }
                content.innerHTML += `
                    <tr>
                        <td class="d-flex flex-column align-items-center" >
                            <div class="card " id="${item.pk}-card" style="width: 18rem;">
                                <div class="card-body">
                                    <h5 class="card-title">${item.fields.title}</h5>
                                    <h6 class="card-subtitle mb-2 text-muted">${item.fields.date}</h6>
                                    <p class="card-text">${item.fields.description}</p>
                                    <h6 class="card-subtitle mb-2 text-muted">${message}</h6>

                                    <a class="btn btn-primary" id='${item.pk}-update' class="card-link">Update</a>
                                    <a  class="btn btn-danger" id='${item.pk}-delete' class="card-link" type="submit">Delete</a>
                                </div>
                            </div>
                        </td>
                    </tr>
                `;
            });
        }
```
8. Menambahkan fungsi JavaScript untuk menambahkan task baru ke dalam database dan menampilkannya ke page
```
function addTask() {
            fetch("{% url 'todolist:add_task' %}", {
                method: "POST",
                body: new FormData(document.querySelector("#form"))
            }).then(refreshTask)
            return false
        }
```
dengan event listener untuk fungsi `addTask()`
```
document.getElementById("submit-modal").onclick = addTask
```