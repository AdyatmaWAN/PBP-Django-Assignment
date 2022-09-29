PBP Tugas 4
=
### Adyatma Wijaksara Aryaputra Nugraha Yudha - 2106750805
### [Web Page](https://pbp-tugas2-adyatma.herokuapp.com/todolist)
Apa kegunaan `{% csrf_token %}` pada elemen `<form>`? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen `<form>`?
-
`{% csrf_token %}` berguna untuk mengenerate token CSRF(Cross Site Request Forgery) yang unik untuk mengamankan aplikasi. Jika ada client yang melakukan request terhadap web server, maka server akan memeriksa apakah token yang dikirimkan oleh client sama dengan token yang ada di cookie. Jika tidak sama, maka request tersebut invalid dan akan ditolak. Jika tidak ada potongan kode tersebut pada elemen `<form>`, maka token CSRF tidak akan tergenerate dan aplikasi tidak akan aman.

Apakah kita dapat membuat elemen `<form>` secara manual (tanpa menggunakan generator seperti `{{ form.as_table }}`)? Jelaskan secara gambaran besar bagaimana cara membuat `<form>` secara manual.
-
Bisa, dengan cara membuat elemen `<form>` dengan menggunakan tag `<form>` dan menambahkan atribut `action` dan `method`. Lalu menggunakan `<input>` untuk menerima inputan dari user serta `<input>` button untuk menyimpan input dari user.
Contoh dari elemen `<form>` yang dibuat secara manual:
```
<form method="POST" action="">
            {% csrf_token %}
            <table>
                <tr>
                    <td>Username:</td>
                    <td><input type="text" name="username" placeholder="Username" class="form-control"></td>
                </tr>

                <tr>
                    <td>Password:</td>
                    <td><input type="password" name="password" placeholder="Password" class="form-control"></td>
                </tr>

                <tr>
                    <td></td>
                    <td><input class="btn login_btn" type="submit" value="Login"></td>
                </tr>
            </table>
        </form>
```

Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.
-
1. Pengguna mengisi form pada halaman html
2. Ketika pengguna menekan tombol submit, maka fungsi `views.py` akan menyimpan data yang diinputkan oleh pengguna. Contoh fungsi untuk menyimpan data yang diinputkan oleh pengguna berdasar models yang dipakai pada tugas ini:
```
todolistitem = TodoListItems(
                user = request.user,
                date = datetime.now(),
                title = form.cleaned_data['tittle'],
                description = form.cleaned_data['description'],
                is_finished = False
            )
```
3. Memanggil method `save()` untuk menyimpan ke dalam database data yang telah diinputkan oleh pengguna.
4. Data yang telah disimpan pada database akan ditampilkan pada halaman html yang menggunakan fungsi di `views.py` yang mengambil isi database.

Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
-
1. Membuat app `todolist` dengan perintah `python manage.py startapp todolist`
2. Tambahkan `todolist` ke dalam `INSTALLED_APPS` pada `settings.py` di `project_django`
3. Tambahkan url pattern `todolist` pada `urls.py` di `project_django`
4. Membuat model `TodoListItems` pada `models.py` di `todolist`
```
class TodoListItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
```
5. Menggunakan `UserCreationForm` untuk register dan fungsi `authenticate` untuk login serta `logout` untuk logout untuk menerapkan register, login, dan logout.
```
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("todolist:show_todolist"))  # membuat response
            response.set_cookie('last_login',
                                str(datetime.now()))  # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response

```
6. Membuat form `CreateTaskForm` pada `forms.py` di `todolist`
```
class CreateTaskForm(forms.Form):
    tittle = forms.CharField()
    description = forms.CharField()
```
7. Membuat templates `create-task.html`, `login.html`, `register.html`, dan `todolist.html`
8. Membuat fungsi `show_todolist` pada `views.py` di `todolist` untuk menampilkan halaman `todolist.html` yang berisi daftar task yang belum selesai dan task yang sudah selesai. Membuat juga fungsi `create_task` untuk menambahkan task baru, fungsi `change_status` untuk merubah status task, dan fungsi `delete-task` untuk menghapus task.
Jangan lupa tambahkan decorator `login_required` pada fungsi `show_todolist`, `create_task`, `change_status`, dan `delete_task` agar hanya user yang sudah login yang dapat mengakses halaman `todolist.html`, dan `create-task.html`.
```
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    data_todolist = TodoListItems.objects.filter(user_id = request.user.id)
    context = {
    'list_todolist': data_todolist,
    'nama': request.user.username,
    'last_login': request.COOKIES['last_login'],
    }
    return render(request, 'todolist.html', context)

@login_required(login_url='/todolist/login/')
def create_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            todolistitem = TodoListItems(
                user = request.user,
                date = datetime.now(),
                title = form.cleaned_data['tittle'],
                description = form.cleaned_data['description'],
                is_finished = False
            )
            todolistitem.save()
            return HttpResponseRedirect("/todolist")
    else:
        form = CreateTaskForm()
    return render(request, "create-task.html", { "form" : form })

@login_required(login_url='/todolist/login/')
def delete_task(request, id):
    todolistitem = TodoListItems.objects.get(id=id)
    todolistitem.delete()
    return HttpResponseRedirect("/todolist")

@login_required(login_url='/todolist/login/')
def change_status(request, id):
    todolistitem = TodoListItems.objects.get(id=id)
    if todolistitem.is_finished:
        todolistitem.is_finished = False
    else:
        todolistitem.is_finished = True
    todolistitem.save()
    return HttpResponseRedirect("/todolist")
```
9. Membuat url pattern untuk `show_todolist`, `create_task`, `change_status`, dan `delete_task` pada `urls.py` di `todolist`
```
urlpatterns = [
    path('', show_todolist, name='show_todolist'),

    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('create-task/', create_task, name='create_task'),
    path('delete_task/<int:id>', delete_task, name='delete_task'),
    path('change_status/<int:id>', change_status, name='change_status')
]
```
