import models.csv as csv
import models.json as json
import models.workers_db as workers_db
import views

workers_db.init()


def workers_list(page=1):
    try:
        all_workers_list = workers_db.get_workers_list()
        workers = workers_db.get_workers_for_page(page, all_workers_list)
        user_answer = views.show_workers_list(workers)
        if user_answer == 1:
            add_worker()
        elif user_answer == 2:
            worker_id = views.worker_id_request()
            more_info(worker_id, page)
        elif user_answer == 3:
            search_param = views.show_search_params()
            query = views.search_query_request()
            search(search_param, query, page)
        elif user_answer == 4:
            workers_list(page + 1)
        elif user_answer == 5:
            workers_list(page - 1)
        elif user_answer == 6:
            import_workers()
        elif user_answer == 7:
            export_workers(page)
        elif user_answer == 0:
            exit()
    except Warning as mes:
        views.show_error(mes)
        workers_list(page)


def add_worker():
    last_name, name, year_of_birth, position, work_phone, salary = views.add_worker()
    try:
        mes = workers_db.add(last_name, name, year_of_birth, position, work_phone, salary)
        views.show_success(mes)
    except Warning as mes:
        views.show_error(mes)
    workers_list()


def more_info(worker_id, page):
    worker_id = int(worker_id)
    try:
        worker_data = workers_db.get_worker_data(worker_id)
        user_answer = views.show_more_info(worker_data)
        if user_answer == 1:
            edit_worker(worker_data, page)
        elif user_answer == 2:
            del_worker(worker_id, page)
        else:
            workers_list(page)
    except Warning as mes:
        views.show_error(mes)
        workers_list(page)


def edit_worker(worker_data, page):
    try:
        worker_new_data = views.edit_worker(worker_data)
        mes = workers_db.edit(worker_new_data)
        views.show_success(mes)
    except Warning as mes:
        views.show_error(mes)
    more_info(worker_data['id'], page)


def del_worker(worker_id, page):
    try:
        mes = workers_db.delete(worker_id)
        views.show_success(mes)
        workers_list()
    except Warning as mes:
        views.show_error(mes)
        more_info(worker_id, page)


def search(search_param, query, page_return, page=1):
    try:
        workers = workers_db.search(search_param, query, page)
        user_answer = views.show_search_result(workers, query)
        if user_answer == 1:
            worker_id = views.worker_id_request()
            more_info(worker_id, page_return)
        elif user_answer == 4:
            search(search_param, query, page_return, page + 1)
        elif user_answer == 5:
            search(search_param, query, page_return, page - 1)
        else:
            workers_list(page_return)
    except Warning as mes:
        views.show_error(mes)
        workers_list(page_return)


def import_workers():
    user_answer = views.file_type_menu()
    file_name = views.file_name_request()
    try:
        if user_answer == 1:
            mes = workers_db.import_workers(file_name, csv.get)
        else:
            mes = workers_db.import_workers(file_name, json.get)
        views.show_success(mes)
    except Warning as msg:
        views.show_error(msg)
    workers_list()


def export_workers(page):
    user_answer = views.file_type_menu()
    file_name = views.file_name_request()
    try:
        if user_answer == 1:
            mes = workers_db.export_workers(file_name, csv.write)
        else:
            mes = workers_db.export_workers(file_name, json.write)
        views.show_success(mes)
    except Warning as msg:
        views.show_error(msg)
    workers_list(page)
