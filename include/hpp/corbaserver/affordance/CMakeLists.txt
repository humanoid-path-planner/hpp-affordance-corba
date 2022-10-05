set(${PROJECT_NAME}_HEADERS fwd.hh server.hh)

install(FILES ${${PROJECT_NAME}_HEADERS}
        DESTINATION include/${CUSTOM_HEADER_DIR})
