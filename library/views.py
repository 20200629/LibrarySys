from django.shortcuts import render,get_object_or_404
from .models import Book,Tag
from users.models import *
from django.views.generic import ListView,DetailView
from django.db.models.aggregates import Count
from django.db.models import Q
# Create your views here.

class IndexView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'book_list'
    paginate_by = 6
 
    #book_list = Book.objects.all().order_by('-create_time')
    #return render(request,'index.html',context={'book_list': book_list})
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'book_list': book_list})，
        这里传递了一个 {'book_list': book_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False    
        right_has_more = False    
        first = False    
        last = False   
    
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:
                        (page_number - 1) if (page_number - 1) > 0 else 0]
        right = page_range[page_number:page_number + 2]

        if right:
            if right[-1] < total_pages:
                last = True        
            if right[-1] < total_pages - 1:
                right_has_more = True    
        if left:
            if left[0] > 1:
                first = True        
            if left[0] > 2:
                left_has_more = True  
    
        data = {'left': left,
                'right': right,        
                'left_has_more': left_has_more,
                'right_has_more': right_has_more, 
                'first': first,       
                'last': last,}

        return data

class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
    context_object_name = 'book'   
    
    #book = get_object_or_404(Book, pk=pk)
    #return render(request, 'detail.html', context={'book': book})

class TagView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class MyBookView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        myself = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super(MyBookView, self).get_queryset().filter(borrower=myself)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    book_list = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, 'index.html', {'error_msg': error_msg,
                                               'book_list': book_list})

def alltags(request):
    tag_list = Tag.objects.annotate(num_books=Count('book'))
    return render(request,'alltags.html',context={'tag_list': tag_list})

def borrow(request):
    q = request.GET.get('q')
    p = request.GET.get('p')
    current_book = Book.objects.get(title=p)
    error_msg = ''
    if not q:
        error_msg = "请登录后再进行此操作"
        return render(request,'is_borrowed.html',context={'current_book': current_book,
                                                           'error_msg': error_msg })

    else:
        current_user = User.objects.get(username=q)
        if  current_book.borrower==current_user:
            error_msg = "你已借阅此书"
        elif current_book.borrower!=current_user:
            error_msg = "此书已被借阅"
        else:
            current_book.borrower = current_user
            current_book.save()
            error_msg = '已经提交申请，请不要重复此操作'
        return render(request,'is_borrowed.html',context={'current_book': current_book,
                                                            'error_msg': error_msg })
