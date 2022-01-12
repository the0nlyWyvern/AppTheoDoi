import pandas as pd
from Google_drive_apis import *
import streamlit as st
from account_management import *
from time_management import * 
from history import *

root_id = '1nj1nzovmwUneexkinlKncUqYoPNj38sS'
log_id = '14CV69oOrf4seWQURppfOjlfr_wlx3ExW'
screen_id = '1RuvD_ik1JkfSs6Stf0chqpjoMztxI4tW'

valid_user = False

def sign_in_error():
    st.warning('Đăng nhập để sử dụng tính năng này')

def print_time_allowed(allowed_time):
    for idx, elem in enumerate(allowed_time):
        st.text(f'Dòng {idx+1}:\n{elem.print()}')

def update_time_txt():
    old_file_id = '1I5Uh8aHXdbpEP-k9y6p3AaXobgjofzDC'
    update('Drive_folder/time.txt', 'time.txt','text/plain',root_id,old_file_id)

def features():
    feature = st.selectbox('Lựa chọn chức năng',options=['Đăng nhập','Thay đổi mật khẩu',
                                                'Xem và thay đổi thời gian sử dụng', 
                                                'Xem lịch sử chụp màn hình',
                                                'Xem lịch sử các phím được sử dụng'])
    if feature == 'Đăng nhập':
        input_pass = st.text_input('Nhập mật khẩu để tiếp tục',type='password')
        pass_button = st.button('Đăng nhập')

        if pass_button:
            find_and_download(root_id,'password.txt','Drive_folder')
            if check_parent_pass(input_pass):
                st.text('Chào mừng phụ huynh đến với chương trình')
            else:
                st.text('Mật khẩu sai, vui lòng nhập lại')

    if feature == 'Thay đổi mật khẩu':
        parent_pass = st.text_input('Nhập mật khẩu mới của phụ huynh (có thể bỏ trống ô này)')
        child_pass = st.text_input('Nhập mật khẩu mới của trẻ (có thể bỏ trống ô này)')
        change_pass_button = st.button('Đổi mật khẩu')
        if change_pass_button:
            if not parent_pass and not child_pass:
                st.text('Bạn cần nhập ít nhất MỘT mật khẩu để tiếp tục')
            else:
                change_password(parent_pass, child_pass)
                old_file_id = '1qvANpdJH0g5_yKyT2O84V2I9nYvxMWpL'
                update('Drive_folder/password.txt', 'password.txt','text/plain',root_id,old_file_id)
                st.success('Thay đổi được cập nhập')

    elif feature == 'Xem và thay đổi thời gian sử dụng':
        st.text('''HƯỚNG DẪN:
+ THÊM THỜI GIAN: Điền vào các ô ngoại trừ ô "Số dòng", sau đó nhấn nút "Thêm"
+ CHỈNH SỬA THỜI GIAN Ở MỘT DÒNG CỤ THỂ: điền số dòng vào ô "Số dòng" và các ô còn lại, sau đó nhấn nút "Thay đổi"
+ XÓA MỘT DÒNG CỤ THỂ: nhập vào ô "Số dòng", để trổng các dòng còn lại, nhấn nút "Thay đổi"''')

        find_and_download(root_id,'time.txt','Drive_folder')
        allowed_time = read_file()
        print_time_allowed(allowed_time)
        st.text('Để thay đổi, nhập số dòng, các thông số khác và nhấn nút "Thay đổi"')
        st.text('Để thêm, nhập các thông số và nhấn nút "Thêm"')

        line_number = st.text_input('Số dòng (Chỉ điền nếu cần thay đổi dòng nào đó, nếu thêm dòng thì không cần điền)')

        F = st.text_input('Giờ bắt đầu (VD: 07:30)')
        T = st.text_input('Giờ kết thúc (VD: 14:10)')
        D = st.text_input('Ngắt sau mỗi (phút): (VD: 60)')
        I = st.text_input('Thời gian nghỉ ngơi (phút): (VD: 10)')
        S = st.text_input('Tổng thời gian sử dụng (phút): (VD: 180)')

        change_time_button = st.button('Thay đổi')
        add_time_button = st.button('Thêm')

        if change_time_button and line_number:
            change_time(allowed_time, int(line_number) - 1, F,T,D,I,S)
            update_time_txt()
            st.success('Thay đổi thành công, quay lại ô "Lựa chọn tính năng", chọn lại tính năng này để xem sự thay đổi')

        if add_time_button:
            add_time(allowed_time, F,T,D,I,S)
            update_time_txt()
            st.success('Thêm thành công, quay lại ô "Lựa chọn tính năng", chọn lại tính năng này để xem sự thay đổi')


    elif feature == 'Xem lịch sử chụp màn hình':
        st.text('Hướng dẫn: Dưới mỗi bức hình là thời gian được chụp lại (giờ-phút-giây)')
        date = st.text_input('Nhập ngày muốn xem lịch sử chụp màn hình (VD: 07-01-2022)')
        screenshot_button = st.button('Xem')
        if screenshot_button:
            if not find_and_download_all(screen_id,date,'Drive_folder/Screen'):
                st.warning('Không tìm thấy ngày này.')
            else:
                valid_names = find_screen(date)
                if not valid_names:
                    st.warning('Không tìm thấy ngày này.')
                else:
                    for name in valid_names:
                        st.image(Image.open(name),caption=f'{name[-12:-4]}')


    elif feature == 'Xem lịch sử các phím được sử dụng':
        date = st.text_input('Nhập ngày muốn xem (VD: 07-01-2022)')
        date += '.txt'
        history_button = st.button('Xem')
        if history_button:
            if not find_and_download_all(log_id,date,'Drive_folder/Log'):
                st.warning('Không tìm thấy ngày này.')
            else:
                date = 'Drive_folder/Log/' + date
                st.text(get_log(date))


def execute_program():
    st.title('APP GIÁM SÁT THỜI GIAN SỬ DỤNG THIẾT BỊ ĐIỆN TỬ CỦA TRẺ')
    st.text('''Thành viên: 
19120549 - Bạch Thiên Khôi
19120557 - Trần Tuấn Kiệt
19120588 - Phạm Duy Minh''')
    st.text('lưu ý: App này đang liên kết với tài khoản drive "apptheodoixD@gmail.com"')
    features()


if __name__ == '__main__':
    execute_program()
    