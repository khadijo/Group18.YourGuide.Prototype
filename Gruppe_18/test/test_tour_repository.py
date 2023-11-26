import os
import uuid

from approvaltests.scrubbers import scrub_all_guids
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Gruppe_18.src.main.model.models import db, Account

import pytest
from approvaltests import verify, Options

from Gruppe_18.src.main.repository.TourRepository import TourRepository
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
import datetime
from Gruppe_18.src.main.model.models import Tour



@pytest.fixture()
def get_session():
    engine = create_engine("sqlite:///Test.db", echo=True)

    Session = sessionmaker(bind=engine)

    return Session()

@pytest.fixture
def tour_re(get_session):
    return TourRepository(get_session)


@pytest.fixture()
def acc_rep(get_session):
    return AccountRepository(get_session)


@pytest.fixture()
def tour():
    return Tour(str(uuid.uuid4()), "Welcome to Dubai",
        datetime.date(2020, 10, 15),
        "Dubai",
        4,
        255,
        15,"English",
        "https://www.hdwallpaper.nu/wp-content/uploads/2015/05/colosseum-1436103.jpg")

# cancellation. return False
@pytest.fixture
def tour_2():
    return Tour(
        str(uuid.uuid4()),
    "Bergen Fjord Exploration",
    datetime.date(2024, 7, 10),
    "Bergen, Norway",
    4,
    4199,
    15,
    "English",
    "https://www.example.com/bergen-fjords.jpg"
)


@pytest.fixture
def tour_3():
    return Tour(
        str(uuid.uuid4()),
    "Discover Oslo's Charm",
    datetime.date(2024, 8, 5),
    "Oslo, Norway",
    2,
    2500,
    10,
    "Norwegian",
    "https://www.example.com/oslo-city.jpg"
)

@pytest.fixture()
def tour_4():
    return Tour(str(uuid.uuid4()),
    "Discover Oslo's Charm",
    datetime.date(2024, 8, 5),
    "Oslo, Norway",
    2,
    2500,
    0,
    "Norwegian",
    "https://www.example.com/oslo-city.jpg"
)

@pytest.fixture()
def guide():
    return Account("1", "guide", "guide", "guide", "12345678","guide@gmial.com")

@pytest.fixture()
def user():
    return Account("2", "user", "user", "user", "12345678", "user@gmial.com")

@pytest.fixture()
def admin():
    return Account("3", "admin", "admin", "admin", "12345678","admin@gmial.com")



@pytest.fixture()
def sqlalchemy_session(tour_re, acc_rep, tour, tour_2, tour_3, guide, user, admin):
    module_path = os.path.dirname(os.path.abspath(__file__))
    database_name = os.path.join(module_path, "Test.db")
    engine = create_engine(f"sqlite:///{database_name}", echo=True)

    session = sessionmaker(bind=engine)()

    db.metadata.create_all(bind=engine)
    tour_re.create_tour(tour)
    tour_re.create_tour(tour_2)
    tour_re.create_tour(tour_3)
    acc_rep.create_account(admin)
    acc_rep.create_account(user)
    acc_rep.create_account(guide)
    yield session

    session.close()
    db.metadata.drop_all(engine)


approval_options = Options().with_scrubber(scrub_all_guids)


# testing feature nonfunctional 1.19 and 1.20
def test_if_tour_is_created_saved_and_retrived(tour_re, sqlalchemy_session):
    saved_data = tour_re.get_all_tours()

    verify(saved_data, options=approval_options)


# testing feature nonfunctional 1.23.1
def test_if_booked_goes_up_by_one_after_registration_to_a_not_fully_booked_tour(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    tour = data[0]
    tour_re.book_tour(tour)
    assert tour.booked == 1


# testing feature nonfunctional 1.24
def test_if_booking_to_fully_booked_tour_is_not_possible(tour_re, sqlalchemy_session, tour_4):
    tour_re.create_tour(tour_4)
    data = tour_re.get_all_tours()
    tour = data[len(data)-1]
    assert tour_re.book_tour(tour) == False


# testing feature nonfunctional 1.22
def test_if_booking_to_none_existing_tour_is_not_possible(tour_re, sqlalchemy_session, tour_4):
    assert tour_re.book_tour(tour_4) == False


# testing feature nonfunctional 1.23.2
def test_if_booked_goes_down_by_one_after_tour_cancelletion(tour_re, sqlalchemy_session):
    tours = tour_re.get_all_tours()
    tour = tours[0]
    tour_re.book_tour(tour)
    assert tour.booked == 1
    tour_re.cancel_booked_tour(tour)
    assert tour.booked == 0


# testing feature nonfunctional 1.17
def test_if_cancellation_on_none_existing_tour_is_not_possible(tour_re, sqlalchemy_session, tour_4):
    assert tour_re.cancel_booked_tour(tour_4) == False


# testing feature 1.19.1.3
def test_if_description_for_a_tour_is_correctly_returnet(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    tour = data[0]
    assert tour_re.get_tour_description(tour.id) == "This tour will take you to Dubai for 4 " \
                                                    "hours, and is offered in English"


# testing feature nonfunctional 1.29
def test_if_getting_description_from_a_non_existing_tour_is_not_possible(tour_re, sqlalchemy_session):
    assert tour_re.get_tour_description("not_existing_id") == "Tour not found"


# testing feature nonfunctional 1.25
def test_if_tour_can_be_deleted_from_database(tour_re, sqlalchemy_session):
    data = tour_re.get_all_tours()
    assert len(data) == 3
    tour_re.delete_tour(data[0].id)
    saved_data = tour_re.get_all_tours()
    assert len(saved_data) == 2


# testing feature non-functional 1.27
def test_if_deleting_none_existing_tour_is_not_possible(tour_re, sqlalchemy_session):
    assert tour_re.delete_tour("not_existing_id") == False


# testing feature 1.8.5
def test_if_filtering_based_on_nothing_returns_all_tours(sqlalchemy_session, tour_re):
    filter_tour = tour_re.filter_combinations('', '', '', '')

    verify(filter_tour, options=approval_options)


# testing feature 1.8.3.1
def test_if_filtering_based_on_only_destination_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("Dubai", "", "", "")
    verify(filter_tour, options=approval_options)


# testing feature 1.8.3.2 and # testing feature 1.8.3.3
def test_if_filtering_based_on_only_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "500", "3000", "")
    verify(filter_tour, options=approval_options)


# testing feature 1.8.3.3
def test_if_filtering_only_on_max_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "", "3000", "")
    verify(filter_tour, options=approval_options)


# testing feature 1.8.3.2
def test_if_filtering_only_on_min_price_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "500", "", "")
    verify(filter_tour, options=approval_options)


# testing feature 1.8.3.4
def test_if_filtering_based_on_only_language_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("", "", "", "English")
    verify(filter_tour, options=approval_options)


# testing feature 1.8.4
def test_if_filtering_based_on_destination_price_and_language_is_as_expected(tour_re, sqlalchemy_session):
    filter_tour = tour_re.filter_combinations("Dubai", "0", "600", "English")
    verify(filter_tour, options=approval_options)


def test_if_getting_spesific_tour_is_possible(tour_re, sqlalchemy_session):
    all_tours = tour_re.get_all_tours()
    tour_1 = all_tours[0]
    tour_1_id = tour_1.id
    assert tour_1 == tour_re.get_specific_tour(tour_1_id)


# testing feature 1.8.5.1
def test_if_searching_tours_by_title_gives_is_as_expected(tour_re, sqlalchemy_session):
    searched_tour = tour_re.search_tour("dubai")
    verify(searched_tour, options=approval_options)


# testing feature nonfunctional 1.30.1
def test_if_guide_and_tour_relationship_gets_made_after_tour_creation(acc_rep, tour_re, sqlalchemy_session, guide):
    all_tours = tour_re.get_all_tours()
    tour_1 = all_tours[0]
    tour_1_id = tour_1.id
    user_id = guide.id
    assert tour_re.guide_register_to_tour(tour_1_id, user_id) == True


# testing feature nonfunctional 1.30.2
def test_if_guide_and_tour_relation_dosent_get_made_for_already_posted_tour(acc_rep, tour_re, sqlalchemy_session, guide):
    all_tours = tour_re.get_all_tours()
    tour_1 = all_tours[0]
    tour_1_id = tour_1.id
    user_id = guide.id
    tour_re.guide_register_to_tour(tour_1_id, user_id)

    all_tours = tour_re.get_all_tours()
    tour_1 = all_tours[0]
    tour_1_id = tour_1.id
    user_id = guide.id
    assert tour_re.guide_register_to_tour(tour_1_id, user_id) == None


# testing feature nonfunctional 1.30.3
def test_if_guide_tour_relation_dosent_get_made_if_tour_or_guide_dosent_exist(tour_re, sqlalchemy_session):
    assert tour_re.guide_register_to_tour("id", "id") == None


# testing feature nonfunctional 1.30.4
def test_if_guide_tour_relationship_gets_deleted_after_tour_get_deleted(tour_re, sqlalchemy_session, guide):
    all_tours = tour_re.get_all_tours()
    tour_1 = all_tours[0]
    tour_1_id = tour_1.id
    user_id = guide.id
    tour_re.guide_register_to_tour(tour_1_id, user_id)

    assert tour_re.guide_delete_tour(tour_1_id, user_id) == True


# testing feature nonfunctional 1.30.3
def test_if_deleting_relation_between_none_existing_tour_and_owner_is_not_possible(tour_re, sqlalchemy_session):
    assert tour_re.guide_delete_tour("id", "id") == None


# testing feature 1.18.10.1
def test_if_admin_gets_correct_number_of_total_users(tour_re, sqlalchemy_session):
    info = tour_re.admin_dashboard()
    assert info['num_users'] == 3


# testing feature 1.18.10.2
def test_if_admin_gets_correct_number_of_tours(tour_re, sqlalchemy_session):
    info = tour_re.admin_dashboard()
    assert info['num_tours'] == 3


# testing feature 1.18.10.4
def test_if_admin_gets_correct_number_of_guides(tour_re, sqlalchemy_session):
    info = tour_re.admin_dashboard()
    assert info['num_guides'] == 1


# testing feature 1.18.10.5
def test_if_admin_gets_correct_number_of_regular_users(tour_re, sqlalchemy_session):
    info = tour_re.admin_dashboard()
    assert info['num_regular_users'] == 1


# testing feature 1.18.10.6
def test_if_admin_gets_correct_number_of_admins(tour_re, sqlalchemy_session):
    info = tour_re.admin_dashboard()
    assert info['num_admin'] == 1


# testing feature 1.18.10.3
def test_if_admin_can_see_number_of_bookings(tour_re, sqlalchemy_session):
    tours = tour_re.get_all_tours()
    tour_re.book_tour(tours[0])
    info = tour_re.admin_dashboard()
    assert info['num_booked_tours'] == 1

